from backend.app.services.budget_service import _category_spending, _percentage


def test_percentage_caps_at_one_hundred() -> None:
    assert _percentage(120, 100) == 100


def test_percentage_handles_zero_total() -> None:
    assert _percentage(50, 0) == 0


def test_category_spending_only_counts_expenses() -> None:
    transactions = [
        {"category": "Food", "amount": 10, "kind": "expense"},
        {"category": "Food", "amount": 100, "kind": "income"},
        {"category": "Transport", "amount": 5, "kind": "expense"},
    ]

    assert _category_spending(transactions) == {"Food": 10, "Transport": 5}
