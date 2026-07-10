from dataclasses import dataclass


CONFLICT_KEYWORDS = {
    "conflict",
    "dilemma",
    "contradiction",
    "tradeoff",
    "trade-off",
    "versus",
    "vs",
    "choice",
    "choose",
    "between",
    "either",
    "or",
    "incompatible",
    "противореч",
    "дилемм",
    "конфликт",
    "выбор",
    "выбрать",
    "между",
    "или",
    "несовместим",
    "уйти",
    "остаться",
}


@dataclass(frozen=True)
class RoutingDecision:
    process_id: str
    reason: str
    matched_keywords: list[str]


def choose_process(problem: str) -> RoutingDecision:
    text = problem.lower()
    matched_keywords = sorted(keyword for keyword in CONFLICT_KEYWORDS if keyword in text)

    if matched_keywords:
        reason = "Detected conflict or dilemma signals: " + ", ".join(matched_keywords)
        return RoutingDecision("goldratt_conflict_cloud", reason, matched_keywords)

    return RoutingDecision(
        "problem_framing",
        "No conflict or dilemma signals detected; using general problem framing.",
        [],
    )
