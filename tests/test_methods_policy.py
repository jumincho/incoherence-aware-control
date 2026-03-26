import unittest

from src.methods import run_method


class MethodTests(unittest.TestCase):
    def setUp(self):
        self.sample = {
            "question": "2+2?",
            "choices": {"A": "1", "B": "2", "C": "4", "D": "5"},
        }
        self.params = {
            "baseline_longcot": {"max_new_tokens": 64, "temperature": 0.2, "top_p": 0.9},
            "hard_cap": {"max_new_tokens": 16, "temperature": 0.2, "top_p": 0.9},
            "self_consistency": {"n_samples": 2, "per_sample_max_new_tokens": 20, "temperature": 0.2, "top_p": 0.9},
            "confidence_select": {"n_samples": 2, "per_sample_max_new_tokens": 20, "temperature": 0.2, "top_p": 0.9},
            "budgeted_self_consistency": {
                "max_rounds": 3,
                "per_sample_max_new_tokens": 20,
                "temperature": 0.2,
                "top_p": 0.9,
            },
            "probe_only_fixedk": {
                "n_probe": 3,
                "per_probe_max_new_tokens": 20,
                "fallback_max_new_tokens": 20,
                "temperature": 0.2,
                "top_p": 0.9,
            },
            "probe_adaptive_k": {
                "initial_k": 2,
                "step_k": 2,
                "k_max": 6,
                "agreement_threshold": 0.75,
                "per_probe_max_new_tokens": 20,
                "fallback_max_new_tokens": 20,
                "temperature": 0.2,
                "top_p": 0.9,
            },
            "forced_deliberation": {
                "initial_max_new_tokens": 20,
                "per_cycle_max_new_tokens": 20,
                "max_rounds": 2,
                "temperature": 0.2,
                "top_p": 0.9,
            },
            "ours_controller": {
                "n_probe": 2,
                "probe_max_new_tokens": 16,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
            },
            "ours_controller_v2": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.15,
                "probe_budget_cap": 64,
                "solve_min_ratio": 0.6,
                "solve_min_floor": 32,
                "low_budget_threshold": 24,
                "enable_low_budget_fallback": True,
                "fallback_hard_cap_tokens": 16,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_controller_v2_nofallback": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.15,
                "probe_budget_cap": 64,
                "solve_min_ratio": 0.6,
                "solve_min_floor": 32,
                "enable_low_budget_fallback": False,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_controller_v2_nofallback_forcecontinue": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.15,
                "probe_budget_cap": 64,
                "min_probe_budget_tokens": 16,
                "solve_min_ratio": 0.6,
                "solve_min_floor": 32,
                "enable_low_budget_fallback": False,
                "force_continue_disagreement_threshold": 0.25,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_controller_v2_nofallback_stopcap": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.15,
                "probe_budget_cap": 64,
                "min_probe_budget_tokens": 16,
                "solve_min_ratio": 0.6,
                "solve_min_floor": 32,
                "enable_low_budget_fallback": False,
                "stop_after_probe_cap_rate": 0.8,
                "stop_cap_disagreement_threshold": 0.25,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_controller_v3": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.10,
                "probe_budget_cap": 48,
                "solve_min_ratio": 0.70,
                "solve_min_floor": 32,
                "low_budget_threshold": 24,
                "enable_low_budget_fallback": True,
                "fallback_hard_cap_tokens": 16,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_controller_v3_nofallback": {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.10,
                "probe_budget_cap": 48,
                "solve_min_ratio": 0.70,
                "solve_min_floor": 32,
                "enable_low_budget_fallback": False,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 128,
            },
            "ours_full": {
                "anchor_stage_cap": 16,
                "decompose_stage_cap": 16,
                "solve_stage_cap": 32,
                "verify_stage_cap": 16,
                "restart_stage_cap": 16,
                "hard_anchor": True,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
            },
        }

    @staticmethod
    def _main(step, prompt, mx, temp, top_p, seed, discarded):
        if "probe" in step:
            return "Tentative Answer: (C)\nConfidence: 0.8"
        if "verify" in step:
            return "Check: PASS\nFinal Answer: (C)\nConfidence: 0.9"
        return "Final Answer: (C)\nConfidence: 0.9"

    @staticmethod
    def _anchor(step, prompt, mx, temp, top_p, seed, discarded):
        return "- Keep units consistent\n- Avoid option mismatch\n- Verify constraints"

    def test_method_runs(self):
        for m in [
            "baseline_longcot",
            "hard_cap",
            "self_consistency",
            "confidence_select",
            "budgeted_self_consistency",
            "probe_only_fixedk",
            "probe_adaptive_k",
            "forced_deliberation",
            "ours_controller",
            "ours_controller_v2",
            "ours_controller_v2_nofallback",
            "ours_controller_v2_nofallback_forcecontinue",
            "ours_controller_v2_nofallback_stopcap",
            "ours_controller_v3",
            "ours_controller_v3_nofallback",
            "ours_full",
            "ours_decompose_only",
            "ours_anchor_only",
        ]:
            p = self.params.get(m, self.params["ours_full"])
            out = run_method(m, self.sample, p, 11, self._main, self._anchor)
            self.assertIn("pred_option", out)
            self.assertIn("response_text", out)

    def test_fallback_equivalence_to_hard_cap(self):
        # When fallback triggers, v2 should be equivalent to hard_cap for same seed/params.
        hard = run_method(
            "hard_cap",
            self.sample,
            {"max_new_tokens": 16, "temperature": 0.2, "top_p": 0.9},
            123,
            self._main,
            self._anchor,
        )
        v2 = run_method(
            "ours_controller_v2",
            self.sample,
            {
                "n_probe": 4,
                "n_probe_first": 2,
                "n_probe_second": 2,
                "probe_max_new_tokens": 16,
                "probe_budget_ratio": 0.15,
                "probe_budget_cap": 64,
                "solve_min_ratio": 0.6,
                "solve_min_floor": 32,
                "low_budget_threshold": 9999,
                "enable_low_budget_fallback": True,
                "fallback_hard_cap_tokens": 16,
                "solve_max_new_tokens": 32,
                "restart_max_new_tokens": 16,
                "stop_conf_threshold": 0.7,
                "max_restart": 1,
                "temperature": 0.2,
                "top_p": 0.9,
                "_budget_total": 512,
            },
            123,
            self._main,
            self._anchor,
        )
        self.assertEqual(hard["pred_option"], v2["pred_option"])
        self.assertEqual(hard["response_text"], v2["response_text"])


if __name__ == "__main__":
    unittest.main()
