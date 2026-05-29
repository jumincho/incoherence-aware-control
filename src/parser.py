"""Answer extraction and parse-policy helpers (the project's `P1R` parser).

Every method in `src.methods` ends with the model emitting raw text. This module
turns that text into a single letter choice — `(A)`, `(B)`, `(C)`, or `(D)` —
or a typed parse-failure reason. Downstream metric code in
`src.analyze_hotmess_style` and `src.report_spend_sweep` then treats parse-fail
rows separately from wrong-answer rows.

The public surface used elsewhere:

- `classify_parse_result(text)` : returns `(option, fail_type, info)`.
  Resolution order, prefer explicit answer markers over free-form mentions:
    1. a bare `A`/`B`/`C`/`D` line,
    2. an explicit "Final Answer: X" / "Tentative Answer: X" line,
    3. keyed phrasings ("answer", "pick", "choose", "therefore ..."),
    4. unique parenthesised `(X)`.
- `extract_final_option(text)`  : convenience wrapper that returns the option
                                  or `None` on parse failure.
- `extract_confidence(text)`    : pulls a `Confidence: <0..1>` value if present.
- `count_flips(seq)` /
  `summarize_answer_trace(texts)` : count how often the answer letter changed
                                    across a sequence of attempts. This is
                                    the per-question raw signal that feeds the
                                    `incoherence` metric.

Parse-failure types (`PARSE_FAIL_*`) are kept stable because they are written
into the per-row JSONL records and the per-round reports compare parse-fail
rates across method × budget cells.
"""

import re
from typing import Dict, List, Optional, Tuple

_OPTION_PATTERN = re.compile(r"\(([ABCDabcd])\)")
_INVALID_PAREN_PATTERN = re.compile(r"\(([A-Za-z])\)")
_CONF_PATTERN = re.compile(r"confidence\s*[:=]\s*([01](?:\.\d+)?)", re.IGNORECASE)
_FINAL_ANSWER_PATTERN = re.compile(
    r"(?:final answer|tentative answer|answer)\s*[:=]\s*\(?([ABCDabcd])\)?",
    re.IGNORECASE,
)
_KEYED_ANSWER_PATTERNS = [
    re.compile(
        r"(?:final answer|final|answer|pick|option|choose|therefore)[^A-Da-d]{0,20}\b([ABCDabcd])\b",
        re.IGNORECASE,
    ),
    re.compile(r"(?:final answer|answer)\s*[:=]\s*\(?([ABCDabcd])\)?", re.IGNORECASE),
]
_SINGLE_OPTION_PATTERN = re.compile(r"^\s*([ABCDabcd])\s*$")
_LAST_OPTION_ANYWHERE_PATTERN = re.compile(r"\(([ABCDabcd])\)|\b([ABCDabcd])\b")

PARSE_FAIL_NO_ANSWER = "NO_ANSWER"
PARSE_FAIL_MULTI_ANSWER = "MULTI_ANSWER"
PARSE_FAIL_INVALID = "INVALID"


def normalize_option(letter: str) -> str:
    return f"({letter.upper()})"


def extract_all_options(text: str) -> List[str]:
    if not text:
        return []
    return [normalize_option(m.group(1)) for m in _OPTION_PATTERN.finditer(text)]


def _extract_keyed_options(text: str) -> List[str]:
    opts: List[str] = []
    if not text:
        return opts
    for pat in _KEYED_ANSWER_PATTERNS:
        matches = pat.findall(text)
        for m in matches:
            opts.append(normalize_option(m))
    return opts


def classify_parse_result(text: str) -> Tuple[Optional[str], Optional[str], Dict[str, object]]:
    """Parse raw model output and classify it as a valid answer choice or a typed failure.

    Accepts the full text of a model response and applies a precedence-ordered extraction
    strategy: (1) a bare single-letter line, (2) an explicit "Final Answer: X" or
    "Tentative Answer: X" marker, (3) keyed phrasings such as "answer", "pick", "choose",
    or "therefore", (4) a unique parenthesised ``(X)`` anywhere in the text. Returns a
    3-tuple of ``(option, fail_type, info)`` where ``option`` is a normalised string such
    as ``"(A)"`` and ``fail_type`` is ``None`` on success or one of the ``PARSE_FAIL_*``
    constants (``NO_ANSWER``, ``MULTI_ANSWER``, ``INVALID``) on failure. ``info`` is a
    diagnostic dict recording the intermediate candidates found at each stage.
    """
    raw_text = text or ""
    m_single = _SINGLE_OPTION_PATTERN.match(raw_text)
    if m_single:
        opt = normalize_option(m_single.group(1))
        return opt, None, {"single_option": opt}

    paren_opts = extract_all_options(raw_text)
    final_line_opts = [normalize_option(x) for x in _FINAL_ANSWER_PATTERN.findall(raw_text)]
    keyed_opts = _extract_keyed_options(raw_text)

    all_opts = paren_opts + keyed_opts
    unique_opts = sorted(set(all_opts))

    info: Dict[str, object] = {
        "final_line_options": final_line_opts,
        "paren_options": paren_opts,
        "keyed_options": keyed_opts,
        "unique_options": unique_opts,
    }

    # Prefer explicit final/tentative answer markers over free-form option mentions in reasoning.
    if final_line_opts:
        return final_line_opts[-1], None, info

    if keyed_opts:
        keyed_unique = sorted(set(keyed_opts))
        if len(keyed_unique) == 1:
            return keyed_unique[0], None, info
        return keyed_opts[-1], None, info

    if len(unique_opts) == 1:
        return unique_opts[0], None, info

    if len(unique_opts) > 1:
        return None, PARSE_FAIL_MULTI_ANSWER, info

    if not raw_text.strip():
        return None, PARSE_FAIL_NO_ANSWER, info

    invalid_candidates = _INVALID_PAREN_PATTERN.findall(raw_text)
    invalid_outside_abcd = [c for c in invalid_candidates if c.upper() not in ["A", "B", "C", "D"]]
    if invalid_outside_abcd:
        info["invalid_candidates"] = invalid_outside_abcd
        return None, PARSE_FAIL_INVALID, info

    if re.search(r"final answer|answer|option|choose|pick", raw_text, re.IGNORECASE):
        return None, PARSE_FAIL_INVALID, info

    return None, PARSE_FAIL_NO_ANSWER, info


def extract_final_option(text: str) -> Optional[str]:
    """Convenience wrapper around ``classify_parse_result`` that returns the option or None.

    Calls ``classify_parse_result(text)`` and returns the normalised option string (e.g.
    ``"(B)"``) when parsing succeeds, or ``None`` when any ``PARSE_FAIL_*`` condition is
    triggered. Use this when callers only need the answer letter and do not need to
    distinguish between failure modes.
    """
    option, fail_type, _ = classify_parse_result(text)
    if fail_type is None:
        return option
    return None


def extract_last_option_anywhere(text: str) -> Optional[str]:
    """Return the last answer letter mentioned anywhere in the text, with no parsing policy applied.

    Scans for any parenthesised ``(X)`` or bare letter ``X`` (A-D, case-insensitive) and
    returns the final match as a normalised option string. This is a fallback heuristic
    used for diagnostics or repair passes; it deliberately ignores the precedence rules in
    ``classify_parse_result`` and can return a letter that appears only in the question
    stem rather than the answer declaration. Returns ``None`` if no letter is found or if
    ``text`` is empty.
    """
    if not text:
        return None
    last = None
    for m in _LAST_OPTION_ANYWHERE_PATTERN.finditer(text):
        cand = m.group(1) or m.group(2)
        if cand:
            last = normalize_option(cand)
    return last


def extract_confidence(text: str) -> Optional[float]:
    """Extract a numeric confidence score from model output if the model declared one.

    Searches for a ``Confidence: <value>`` or ``Confidence = <value>`` pattern
    (case-insensitive) and returns the parsed float clamped to ``[0.0, 1.0]``. Returns
    ``None`` if no confidence declaration is found or if ``text`` is empty. The confidence
    value is used by the controller to decide whether to continue sampling; it is not
    required for plain accuracy measurement.
    """
    if not text:
        return None
    m = _CONF_PATTERN.search(text)
    if not m:
        return None
    val = float(m.group(1))
    if val < 0:
        return 0.0
    if val > 1:
        return 1.0
    return val


def option_to_index(option: Optional[str]) -> Optional[int]:
    if option is None:
        return None
    lookup = {"(A)": 0, "(B)": 1, "(C)": 2, "(D)": 3}
    return lookup.get(option)


def index_to_option(idx: int) -> str:
    return ["(A)", "(B)", "(C)", "(D)"][idx]


def count_flips(options: List[str]) -> int:
    if len(options) <= 1:
        return 0
    flips = 0
    prev = options[0]
    for cur in options[1:]:
        if cur != prev:
            flips += 1
        prev = cur
    return flips


def summarize_answer_trace(texts: List[str]) -> Tuple[List[str], int]:
    seq: List[str] = []
    for text in texts:
        seq.extend(extract_all_options(text))
    return seq, count_flips(seq)
