from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.db import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

# POST: create new transaction
@router.post("/")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_tx = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id=transaction.category_id,
        user_id=1,  # hardcoded for now
        description=transaction.description,
        date=transaction.date
    )

    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    return new_tx

# GET: get all transactions
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).options(joinedload(Transaction.category)).all()

# GET: get single transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    return tx

# DELETE: remove transaction from database
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not tx:
        return {"error": "Transaction not found"}

    db.delete(tx)
    db.commit()

    return {"message": "Deleted"}