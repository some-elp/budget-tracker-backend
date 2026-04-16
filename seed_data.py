from db import SessionLocal
from models.user import User
from models.category import Category
from models.transaction import Transaction

session = SessionLocal()

# Create users
alice = User(email="alice@test.com", password_hash="hashed")
bob = User(email="bob@test.com", password_hash="hashed")

session.add_all([alice, bob])
session.commit()

# Create categories
food = Category(name="Food", user_id=alice.id)
rent = Category(name="Rent", user_id=alice.id)
salary = Category(name="Salary", user_id=alice.id)

gaming = Category(name="Gaming", user_id=bob.id)
groceries = Category(name="Groceries", user_id=bob.id)

session.add_all([food, rent, salary, gaming, groceries])
session.commit()

# Create transactions
t1 = Transaction(amount=2000, type="income", user_id=alice.id, category_id=salary.id)
t2 = Transaction(amount=50, type="expense", user_id=alice.id, category_id=food.id)
t3 = Transaction(amount=1200, type="expense", user_id=alice.id, category_id=rent.id)

t4 = Transaction(amount=70, type="expense", user_id=bob.id, category_id=gaming.id)
t5 = Transaction(amount=100, type="expense", user_id=bob.id, category_id=groceries.id)

session.add_all([t1, t2, t3, t4, t5])
session.commit()

print("Seed data inserted!")