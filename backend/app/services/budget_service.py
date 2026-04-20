from calendar import monthrange
from datetime import date
from uuid import uuid4

from fastapi import HTTPException

from backend.app.core.storage import store
from backend.app.models import (
    BudgetCreate,
    GoalCreate,
    RecurringItemCreate,
    TransactionCreate,
    TransactionKind,
)


COLLECTIONS = {
    "transactions",
    "budgets",
    "goals",
    "recurring_items",
}


def list_items(collection: str) -> list[dict]:
    _validate_collection(collection)
    return store.read()[collection]


def create_item(collection: str, item: TransactionCreate | BudgetCreate | GoalCreate | RecurringItemCreate) -> dict:
    _validate_collection(collection)
    data = store.read()
    new_item = {"id": uuid4().hex, **item.model_dump(mode="json")}
    data[collection].append(new_item)
    store.write(data)
    return new_item


def delete_item(collection: str, item_id: str) -> None:
    _validate_collection(collection)
    data = store.read()
    original_count = len(data[collection])
    data[collection] = [item for item in data[collection] if item["id"] != item_id]

    if len(data[collection]) == original_count:
        raise HTTPException(status_code=404, detail="Item not found")

    store.write(data)


def get_summary(month: str | None = None) -> dict:
    data = store.read()
    today = date.today()
    year, month_number = _parse_month(month, today)
    start = date(year, month_number, 1)
    end = date(year, month_number, monthrange(year, month_number)[1])

    transactions = [
        transaction
        for transaction in data["transactions"]
        if start <= date.fromisoformat(transaction["date"]) <= end
    ]

    total_income = _sum_kind(transactions, TransactionKind.income)
    total_expenses = _sum_kind(transactions, TransactionKind.expense)
    net_cashflow = total_income - total_expenses
    total_budgeted = sum(budget["monthly_limit"] for budget in data["budgets"])

    category_spending = _category_spending(transactions)
    budget_status = [
        {
            "category": budget["category"],
            "monthly_limit": budget["monthly_limit"],
            "spent": category_spending.get(budget["category"], 0),
            "remaining": budget["monthly_limit"] - category_spending.get(budget["category"], 0),
        }
        for budget in data["budgets"]
    ]

    goals = [
        {
            **goal,
            "progress": _percentage(goal["saved_amount"], goal["target_amount"]),
            "remaining": max(goal["target_amount"] - goal["saved_amount"], 0),
        }
        for goal in data["goals"]
    ]

    return {
        "month": f"{year}-{month_number:02d}",
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_cashflow": round(net_cashflow, 2),
        "total_budgeted": round(total_budgeted, 2),
        "budget_status": budget_status,
        "goals": goals,
        "upcoming_recurring": sorted(data["recurring_items"], key=lambda item: item["day_of_month"]),
        "recent_transactions": sorted(transactions, key=lambda item: item["date"], reverse=True)[:8],
    }


def _validate_collection(collection: str) -> None:
    if collection not in COLLECTIONS:
        raise HTTPException(status_code=404, detail="Collection not found")


def _parse_month(month: str | None, today: date) -> tuple[int, int]:
    if not month:
        return today.year, today.month

    try:
        year_text, month_text = month.split("-", 1)
        year = int(year_text)
        month_number = int(month_text)
        if not 1 <= month_number <= 12:
            raise ValueError
        return year, month_number
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Month must use YYYY-MM format") from exc


def _sum_kind(transactions: list[dict], kind: TransactionKind) -> float:
    return sum(item["amount"] for item in transactions if item["kind"] == kind)


def _category_spending(transactions: list[dict]) -> dict[str, float]:
    spending: dict[str, float] = {}
    for item in transactions:
        if item["kind"] != TransactionKind.expense:
            continue
        spending[item["category"]] = spending.get(item["category"], 0) + item["amount"]
    return spending


def _percentage(value: float, total: float) -> float:
    if total == 0:
        return 0
    return round(min(value / total * 100, 100), 1)
