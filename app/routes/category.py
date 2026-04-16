from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.models.category import Category

router  = APIRouter()

# POST: Create a new category
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(
        name=category.name,
        user_id=1 # hardcoded
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# GET: get all categories
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.user_id == 1).all()

# GET: get one category by ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category =  db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == 1
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

# DELETE: delete category by ID
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == 1
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Deleted"}
