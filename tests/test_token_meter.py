import unittest

from src.token_meter import TokenBudget


class TokenMeterTests(unittest.TestCase):
    def test_budget_accounting_total(self):
        b = TokenBudget(total_limit=100)
        self.assertTrue(b.can_generate())
        self.assertEqual(b.remaining_total(), 100)

        # If prompt consumes 30, at most 70 new tokens are available.
        self.assertEqual(b.clip_max_new_tokens(1000, prompt_tokens=30), 70)

        b.add("solve.baseline", role="solve", input_tokens=30, output_tokens=40)
        b.add("probe.controller.0", role="probe", input_tokens=10, output_tokens=20, discarded=True)

        self.assertEqual(b.total_spent, 100)
        self.assertEqual(b.output_spent, 60)
        self.assertEqual(b.input_spent, 40)
        self.assertEqual(b.remaining_total(), 0)
        self.assertFalse(b.can_generate())

    def test_stage_spend(self):
        b = TokenBudget(total_limit=200)
        b.add("probe.controller.0", role="probe", input_tokens=10, output_tokens=5)
        b.add("probe.controller.1", role="probe", input_tokens=12, output_tokens=6)
        b.add("solve.controller", role="solve", input_tokens=20, output_tokens=30)

        s = b.stage_spend()
        self.assertEqual(s["probe"]["calls"], 2)
        self.assertEqual(s["probe"]["total_tokens"], 33)
        self.assertEqual(s["solve"]["calls"], 1)
        self.assertEqual(s["solve"]["total_tokens"], 50)


if __name__ == "__main__":
    unittest.main()
