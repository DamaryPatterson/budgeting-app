from fastapi import APIRouter, Response

from backend.app.models import (
    Budget,
    BudgetCreate,
    Goal,
    GoalCreate,
    RecurringItem,
    RecurringItemCreate,
    Transaction,
    TransactionCreate,
)
from backend.app.services.budget_service import create_item, delete_item, get_summary, list_items


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/summary")
def summary(month: str | None = None) -> dict:
    return get_summary(month)


@router.get("/transactions", response_model=list[Transaction])
def transactions() -> list[dict]:
    return list_items("transactions")


@router.post("/transactions", response_model=Transaction, status_code=201)
def add_transaction(transaction: TransactionCreate) -> dict:
    return create_item("transactions", transaction)


@router.delete("/transactions/{transaction_id}", status_code=204)
def remove_transaction(transaction_id: str) -> Response:
    delete_item("transactions", transaction_id)
    return Response(status_code=204)


@router.get("/budgets", response_model=list[Budget])
def budgets() -> list[dict]:
    return list_items("budgets")


@router.post("/budgets", response_model=Budget, status_code=201)
def add_budget(budget: BudgetCreate) -> dict:
    return create_item("budgets", budget)


@router.delete("/budgets/{budget_id}", status_code=204)
def remove_budget(budget_id: str) -> Response:
    delete_item("budgets", budget_id)
    return Response(status_code=204)


@router.get("/goals", response_model=list[Goal])
def goals() -> list[dict]:
    return list_items("goals")


@router.post("/goals", response_model=Goal, status_code=201)
def add_goal(goal: GoalCreate) -> dict:
    return create_item("goals", goal)


@router.delete("/goals/{goal_id}", status_code=204)
def remove_goal(goal_id: str) -> Response:
    delete_item("goals", goal_id)
    return Response(status_code=204)


@router.get("/recurring-items", response_model=list[RecurringItem])
def recurring_items() -> list[dict]:
    return list_items("recurring_items")


@router.post("/recurring-items", response_model=RecurringItem, status_code=201)
def add_recurring_item(item: RecurringItemCreate) -> dict:
    return create_item("recurring_items", item)


@router.delete("/recurring-items/{item_id}", status_code=204)
def remove_recurring_item(item_id: str) -> Response:
    delete_item("recurring_items", item_id)
    return Response(status_code=204)
