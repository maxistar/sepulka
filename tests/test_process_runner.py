import unittest

from sepulka.process_runner import ProcessRunner, response_language_hint


PROCESS = {
    "id": "problem_framing",
    "name": "Problem Framing",
    "description": "Clarifies a problem.",
    "steps": [
        {"id": "one", "name": "One", "prompt": "Analyze the problem."},
    ],
    "expected_outputs": ["answer"],
}


class FakeLLM:
    def __init__(self) -> None:
        self.calls = []

    def chat(self, messages, temperature=0.2):
        self.calls.append(messages)
        return "ok"


class ProcessRunnerTests(unittest.TestCase):
    def test_language_hint_detects_russian(self) -> None:
        self.assertEqual(
            response_language_hint("Я не знаю, что делать"),
            "Respond in Russian unless the user explicitly requested another language.",
        )

    def test_language_hint_detects_english(self) -> None:
        self.assertEqual(
            response_language_hint("I need to frame this problem"),
            "Respond in English unless the user explicitly requested another language.",
        )

    def test_prompts_include_language_instruction(self) -> None:
        fake_llm = FakeLLM()
        ProcessRunner(fake_llm).run("Я выбираю между двумя вариантами", PROCESS, [])

        prompts = "\n\n".join(message["content"] for call in fake_llm.calls for message in call)
        self.assertIn("Respond in Russian", prompts)


if __name__ == "__main__":
    unittest.main()
