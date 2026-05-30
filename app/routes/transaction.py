from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from app.db import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.schemas.summary import TransactionSummary
from app.models.category import Category
from app.core.deps import get_current_user
from app.models.user import User
from datetime import date
from typing import Literal

router = APIRouter()

# POST: create new transaction
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
      Category.id == transaction.category_id,
      Category.user_id == current_user.id
    ).first()

    if not category:
      raise HTTPException(status_code=400, detail ="Invalid category_id")

    new_tx = Transaction(
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        category_id=transaction.category_id,
        user_id=current_user.id,
        description=transaction.description,
        date=transaction.date
    )

    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    return new_tx

# GET: get all transactions
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    transaction_type: Literal["income", "expense"] | None = None,
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    query = db.query(Transaction)\
        .options(joinedload(Transaction.category))\
        .filter(Transaction.user_id == current_user.id)\
        .order_by(Transaction.date.desc())
    
    if transaction_type is not None:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)

    if start_date is not None:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date is not None:
        query = query.filter(Transaction.date <= end_date)

    return query.all()

# GET: get transactions summary
@router.get("/summary", response_model=TransactionSummary)
def get_transaction_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income_total = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "income"
    ).scalar()

    expense_total = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense"
    ).scalar()

    income_total = income_total or 0
    expense_total = expense_total or 0

    return {
        "total_income": income_total,
        "total_expenses": expense_total,
        "balance": income_total - expense_total
    }

# GET: get single transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction)\
        .options(joinedload(Transaction.category))\
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        ).first()

    if not tx:
      raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

# DELETE: remove transaction from database
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id ==  current_user.id
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()

    return {"message": "Deleted"}

# PATCH: Update transaction by ID
@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    update_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    tx = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if update_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == update_data.category_id,
            Category.user_id == current_user.id
        ).first()

        if not category:
            raise HTTPException(status_code=400, detail="Invalid category_id")
        
    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(tx, field, value)

    db.commit()
    updated_tx = db.query(Transaction)\
        .options(joinedload(Transaction.category))\
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        ).first()

    return updated_tx