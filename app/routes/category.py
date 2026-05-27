from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.category import Category
from app.core.deps import get_current_user
from app.models.user import User

router  = APIRouter()

# POST: Create a new category
@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_category = Category(
        name=category.name,
        user_id=current_user.id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# GET: get all categories
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Category).filter(Category.user_id == current_user.id).all()

# GET: get one category by ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category =  db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

# DELETE: delete category by ID
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Deleted"}

# PATCH: update category by ID
@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    update_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category

