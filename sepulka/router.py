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


def choose_process(problem: str) -> str:
    text = problem.lower()
    if any(keyword in text for keyword in CONFLICT_KEYWORDS):
        return "goldratt_conflict_cloud"
    return "problem_framing"
