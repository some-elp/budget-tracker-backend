from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float, String, Date
from datetime import date
from app.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    amount: Mapped[float] = mapped_column(nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)  # "income" or "expense"
    date: Mapped[date] = mapped_column(Date, default=date.today)
    description: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # ORM Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")