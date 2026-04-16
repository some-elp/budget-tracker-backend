from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
    categories = relationship("Category", back_populates="user", cascade="all, delete")