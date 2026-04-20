from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field


Money = Annotated[float, Field(ge=0)]


class TransactionKind(StrEnum):
    income = "income"
    expense = "expense"


class TransactionBase(BaseModel):
    date: date
    description: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=60)
    amount: Money
    kind: TransactionKind


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: str


class BudgetBase(BaseModel):
    category: str = Field(min_length=1, max_length=60)
    monthly_limit: Money


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: str


class GoalBase(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    target_amount: Money
    saved_amount: Money = 0


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: str


class RecurringItemBase(BaseModel):
    description: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=60)
    amount: Money
    kind: TransactionKind
    day_of_month: int = Field(ge=1, le=31)


class RecurringItemCreate(RecurringItemBase):
    pass


class RecurringItem(RecurringItemBase):
    id: str
