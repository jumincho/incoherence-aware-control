from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TokenEvent:
    step: str
    role: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    discarded: bool = False


@dataclass
class TokenBudget:
    total_limit: int
    total_spent: int = 0
    output_spent: int = 0
    input_spent: int = 0
    events: List[TokenEvent] = field(default_factory=list)

    def remaining_total(self) -> int:
        return max(0, self.total_limit - self.total_spent)

    def can_generate(self) -> bool:
        return self.remaining_total() > 0

    def clip_max_new_tokens(self, requested: int, prompt_tokens: int) -> int:
        allowed = max(0, self.remaining_total() - int(prompt_tokens))
        return max(0, min(int(requested), allowed))

    def add(
        self,
        step: str,
        role: str,
        input_tokens: int,
        output_tokens: int,
        discarded: bool = False,
    ) -> None:
        input_tokens = int(input_tokens)
        output_tokens = int(output_tokens)
        total_tokens = input_tokens + output_tokens

        self.input_spent += input_tokens
        self.output_spent += output_tokens
        self.total_spent += total_tokens

        self.events.append(
            TokenEvent(
                step=step,
                role=role,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                discarded=discarded,
            )
        )

    def usage_dict(self) -> Dict[str, int]:
        return {
            "input_tokens": int(self.input_spent),
            "output_tokens": int(self.output_spent),
            "total_tokens": int(self.total_spent),
        }

    def stage_spend(self) -> Dict[str, Dict[str, int]]:
        agg: Dict[str, Dict[str, int]] = {}
        for e in self.events:
            if e.role not in agg:
                agg[e.role] = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
            agg[e.role]["calls"] += 1
            agg[e.role]["input_tokens"] += e.input_tokens
            agg[e.role]["output_tokens"] += e.output_tokens
            agg[e.role]["total_tokens"] += e.total_tokens
        return agg

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_limit": int(self.total_limit),
            "total_spent": int(self.total_spent),
            "output_spent": int(self.output_spent),
            "input_spent": int(self.input_spent),
            "events": [
                {
                    "step": e.step,
                    "role": e.role,
                    "input_tokens": e.input_tokens,
                    "output_tokens": e.output_tokens,
                    "total_tokens": e.total_tokens,
                    "discarded": e.discarded,
                }
                for e in self.events
            ],
        }
