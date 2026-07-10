import unittest

from sepulka.router import choose_process


class RouterTests(unittest.TestCase):
    def test_conflict_keywords_select_conflict_cloud(self) -> None:
        decision = choose_process("Уйти с работы или остаться ради стабильности?")

        self.assertEqual(decision.process_id, "goldratt_conflict_cloud")
        self.assertIn("или", decision.matched_keywords)
        self.assertIn("Detected conflict", decision.reason)

    def test_default_selects_problem_framing(self) -> None:
        decision = choose_process("Мне нужно лучше понять проблему с учебным проектом")

        self.assertEqual(decision.process_id, "problem_framing")
        self.assertEqual(decision.matched_keywords, [])
        self.assertIn("No conflict", decision.reason)


if __name__ == "__main__":
    unittest.main()
