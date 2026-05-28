from pydantic import BaseModel, Field
from datetime import date as Date
from typing import Optional, Literal
from app.schemas.category import CategoryResponse


class TransactionCreate(BaseModel):
    amount: float
    transaction_type: Literal["income", "expense"]
    category_id: int
    description: Optional[str] = None
    date: Date = Field(default_factory=Date.today)

class TransactionResponse(BaseModel):
    id: int
    amount: float
    transaction_type: str
    description: Optional[str]
    date: Date | None

    category: CategoryResponse

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    amount: float | None = None
    transaction_type: Literal["income", "expense"] | None = None
    category_id: int | None = None
    description: str | None = None
    date: Date | None = None