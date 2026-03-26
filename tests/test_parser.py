import unittest

from src.parser import (
    PARSE_FAIL_INVALID,
    PARSE_FAIL_MULTI_ANSWER,
    PARSE_FAIL_NO_ANSWER,
    classify_parse_result,
    extract_final_option,
    extract_last_option_anywhere,
)


class ParserTests(unittest.TestCase):
    def test_20_answer_formats(self):
        cases = [
            ("Final Answer: (A)", "(A)"),
            ("The answer is (B).", "(B)"),
            ("Therefore, (C)", "(C)"),
            ("Ans: (D)", "(D)"),
            ("Reasoning...\\nFinal Answer:(A)", "(A)"),
            ("Answer = (B)", "(B)"),
            ("I choose (C).", "(C)"),
            ("Best option: (D)", "(D)"),
            ("(A)", "(A)"),
            ("foo bar (B) baz", "(B)"),
            ("Some text\\n(A) then (A)", "(A)"),
            ("\\\\boxed{(D)}", "(D)"),
            ("Final: C", "(C)"),
            ("thus answer D", "(D)"),
            ("Pick A", "(A)"),
            ("pick: b", "(B)"),
            ("Option c", "(C)"),
            ("my final is d", "(D)"),
            ("No option yet (B) but revised (B)", "(B)"),
            ("Output\\nFinal Answer: (D)\\nConfidence: 0.7", "(D)"),
            ("Final Answer: A", "(A)"),
            ("Final Answer: c", "(C)"),
            ("A", "(A)"),
            (" d ", "(D)"),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(extract_final_option(text), expected)

    def test_multi_answer(self):
        opt, fail, _ = classify_parse_result("Final Answer: (A) ... revised ... (C)")
        self.assertEqual(opt, "(A)")
        self.assertIsNone(fail)

        opt2, fail2, _ = classify_parse_result("I think (A) or maybe (C)")
        self.assertIsNone(opt2)
        self.assertEqual(fail2, PARSE_FAIL_MULTI_ANSWER)

    def test_invalid(self):
        opt, fail, _ = classify_parse_result("Final Answer: (E)")
        self.assertIsNone(opt)
        self.assertEqual(fail, PARSE_FAIL_INVALID)

    def test_no_answer(self):
        opt, fail, _ = classify_parse_result("This is a reasoning paragraph with no label.")
        self.assertIsNone(opt)
        self.assertEqual(fail, PARSE_FAIL_NO_ANSWER)

    def test_extract_last_option_anywhere(self):
        self.assertEqual(extract_last_option_anywhere("reason (A) then final B"), "(B)")
        self.assertEqual(extract_last_option_anywhere("Pick c"), "(C)")
        self.assertIsNone(extract_last_option_anywhere("no option"))


if __name__ == "__main__":
    unittest.main()
