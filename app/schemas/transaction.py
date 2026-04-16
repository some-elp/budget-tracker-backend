from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
from app.schemas.category import CategoryResponse


class TransactionCreate(BaseModel):
    amount: float
    type: Literal["income", "expense"]
    category_id: int
    description: Optional[str] = None
    date: Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    description: Optional[str]
    date: Optional[datetime]

    category: CategoryResponse

    class Config:
        from_attributes = True