from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

# POST: create new transaction
@router.post("/")
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
        type=transaction.type,
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
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Transaction)\
    .options(joinedload(Transaction.category))\
    .filter(Transaction.user_id == current_user.id)\
    .all()

# GET: get single transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tx = db.query(Transaction).filter(
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
        Transaction.id = transaction_id,
        Transaction.user_id = current_user.id
    ).first()

    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if update_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == update_date.category_id,
            Category.user_id == current_user.id
        ).first()

        if not category:
            raise HTTPException(status_code=400, detail="Invalid category_id")
        
    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(tx, field, value)

    db.commit()
    db.refresh(tx)

    return tx