from app.db import engine, Base
import app.models.user
import app.models.category
import app.models.transaction

Base.metadata.create_all(engine)