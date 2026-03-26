# Incoherence-Aware Test-Time Control Closure Report

Date: 2026-03-27  
Archived from: `/workspace/incoh-pilot-transfer-repo`

## 1. Executive Summary

This project studied **incoherence-aware test-time control for multiple-choice reasoning**.

The main research idea was:

- run multiple reasoning probes or controller steps at test time
- measure instability through an `incoherence` quantity, described throughout the project as roughly `variance / error`
- use budget-aware control to reduce incoherence without sacrificing, and ideally improving, final accuracy

The strongest final reading is:

- **A regime-dependent controller effect is real.**
- Under stricter and cleaner protocols in the later rounds, the controller family reduced incoherence reliably.
- In the latest setup, **accuracy plus incoherence improved together only in sufficiently high-budget regimes**, not uniformly at all budgets.
- The stronger “dynamic novelty” claim, especially versus strong probe-only baselines, remained mixed.

So this project did not end as “the controller always wins.” It ended as a narrower but still meaningful result:

> Incoherence-aware test-time control can help, but the gain is strongly budget-regime-dependent and not a universal dominance result.

## 2. What This Project Was

The repository is a transfer package for a multi-round experiment series, spanning roughly **Rounds 1 through 9**.

The research question was whether a controller can use extra test-time reasoning budget more intelligently than simpler baselines such as:

- `hard_cap`
- `hard_cap_matched`
- `probe_only_fixedk_k{2,4,8}`
- `probe_adaptive_k_selected`
- `budgeted_self_consistency`

The main “ours” family evolved over time:

- `ours_controller`
- `ours_controller_v2_nofallback`
- `ours_controller_v3_nofallback`

The primary evaluation datasets in the later rounds were:

- `GPQA`
- `MMLU` as a secondary reproduction benchmark

The project also emphasized fairness and hygiene controls:

- unified token accounting
- frozen parser/repair policy
- parse-fail reporting
- held-out splits
- pre-registration
- code-lock manifests

## 3. Main Code

The key files are:

- `src/run_pilot.py`: experiment runner and sharded execution
- `src/methods.py`: baseline and controller method definitions
- `src/parser.py`: answer extraction and parse-policy logic
- `src/token_meter.py`: token accounting and budget tracking
- `src/analyze_hotmess_style.py`: incoherence and variance-style analysis
- `src/report_spend_sweep.py`: detailed budget-sweep reporting

Operationally important folders are:

- `configs/`: round-specific configs
- `scripts/`: pipeline launch helpers
- `reports/`: detailed round reports, preregistration, and code-lock artifacts
- `docs/`: handover and reproduction guides

## 4. How The Story Evolved

### Rounds 1 to 4

These rounds established feasibility and hardened the measurement setup.

Main outcomes:

- there was an early signal that controller-like methods could reduce instability
- token accounting, parser behavior, and identity/fairness issues mattered a lot
- the project learned that many apparent gains could be distorted by parse behavior or accounting inconsistencies unless the protocol was tightened

At this stage, the project was promising but methodologically unfinished.

### Rounds 5 to 7

These rounds formalized a more publication-like protocol:

- preregistration
- code lock
- held-out splits
- cleaner governance around what could be claimed

The result was a stronger and more honest narrative:

- the controller seemed promising
- but the exact transition point where it helped depended on the protocol
- stronger baselines and cleaner controls narrowed the claim

### Round 8

Round 8 is one of the most important rounds in the repository.

It introduced:

- a fresh pool and split
- stricter fairness controls
- strict formatter / repair reserve
- unified token accounting
- a matched hard-cap baseline
- a second-benchmark reproduction

The most important Round 8 result:

- on held-out `GPQA` B3, `ours_controller_v2_nofallback` improved both accuracy and incoherence relative to `hard_cap` starting around `T*=400`
- parse fail was effectively controlled to zero in the core held-out budgets
- the `MMLU` reproduction also showed the same qualitative direction against the hard-cap family

But an important limitation remained:

- superiority over strong probe-only baselines was still mixed rather than cleanly decisive

### Round 9

Round 9 is the latest and most relevant final state of the project.

It introduced:

- a fresh split again
- `ours_controller_v3_nofallback`
- new pre-registration
- new code lock
- a held-out GPQA run
- a confirm run on key budgets
- another MMLU reproduction

The main Round 9 held-out result was more nuanced than Round 8:

- the transition threshold versus `hard_cap` moved upward to about `T*=900`
- below that, the controller often reduced incoherence but paid an accuracy cost
- at high budgets such as `900` and `1500`, the controller improved both accuracy and incoherence over `hard_cap`

Representative held-out GPQA B9 deltas versus `hard_cap`:

- Budget `900`: `Δacc = +0.0986`, `Δincoh = -0.1409`
- Budget `1500`: `Δacc = +0.1081`, `Δincoh = -0.1551`

At the same time:

- parse fail was `0`
- repair success was effectively perfect in the final held-out runs
- the confirm run focused on lower budgets and remained negative on accuracy there
- the dynamic-over-probe story was still not fully settled

This led to the project’s most defensible final position:

- the controller effect is **real but regime-dependent**
- the transition threshold is **not universal**
- dynamic novelty over strong probe-only baselines is **still mixed**

## 5. What Was Actually Learned

### Strongest supported claim

The best-supported claim is:

> Under strict accounting and parse controls, incoherence-aware controller methods can outperform hard-cap baselines in sufficiently high-budget regimes.

Why this is credible:

- it survived multiple later-round protocol tightenings
- Round 8 and Round 9 both showed a threshold-style phenomenon
- the direction also reproduced on a second benchmark
- parse confounds were no longer driving the effect in the final rounds

### Important qualification

The threshold is not stable across protocol versions.

In the project’s own records:

- Round 8 suggested a transition near `T≈400`
- Round 9 suggested a transition near `T≈900`

This means the threshold should be interpreted as:

- a **configuration/protocol-dependent regime boundary**

and not as:

- a universal scientific constant

### Weak or unresolved claim

The weaker claim is:

> The dynamic controller cleanly dominates strong probe-only baselines.

That did not become fully convincing.

The project itself repeatedly notes:

- probe-only families remained very strong
- controller novelty beyond probe-only selection was not fully settled
- some budgets still showed strong incoherence improvement with noticeable accuracy loss

So the repository supports a careful systems-style claim more than a sweeping dominance claim.

## 6. Why This Project Is Being Archived

This line of work produced meaningful knowledge, but its outcome narrowed over time.

Reasons to archive rather than continue this exact repo as an active project:

1. The final claim is narrower than the most ambitious early framing.
2. The most interesting result is regime-aware, not universal.
3. The strongest novelty claim over probe-only baselines remains incomplete.
4. The repository already functions more as a handoff / transfer package than a living codebase.

That does not mean the project failed. It means the final honest contribution is more precise:

- a robust methodology
- a cleaner protocol
- and a real but conditional controller effect

## 7. Final Status At Closure

At closure, the clearest interpretation is:

- this is a mature experiment archive
- Round 9 is the best final baseline
- `ours_controller_v3_nofallback` is the latest serious method
- the high-budget hard-cap comparison looks real
- the dynamic-over-probe novelty claim remains mixed

If someone asked, “What should I believe after reading this repository?” the best answer is:

- Believe that **incoherence-aware test-time control can help under the right budget regime and a clean protocol**.
- Do not believe that the controller was shown to **uniformly dominate all strong baselines at all budgets**.

## 8. What Is Preserved In This Closure Bundle

This bundle intentionally keeps the project small enough for archival use while preserving the most important material.

It includes:

- full core code in `src/`
- configs, scripts, tests, and docs
- all round reports and governance artifacts
- selected summary-only run artifacts from key Round 8 and Round 9 runs
- this closure report in English and Korean

It excludes the full raw `runs/` tree, which was much larger and mostly redundant for understanding the project’s final state.

## 9. Bottom Line

This project is best remembered as a careful attempt to turn “reasoning instability” into something measurable and controllable under test-time compute budgets.

The lasting result is not “controller always wins.”

It is:

- **controller gains are real under strict protocol**
- **those gains are regime-dependent**
- **high-budget wins over hard-cap baselines are the strongest final result**
- **full novelty over probe-only families remains unresolved**

That is the most accurate newcomer-friendly summary of the repository at closure.
