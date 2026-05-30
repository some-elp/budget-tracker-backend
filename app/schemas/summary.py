from pydantic import BaseModel

class TransactionSummary(BaseModel):
  total_income: float
  total_expenses: float
  balance: float