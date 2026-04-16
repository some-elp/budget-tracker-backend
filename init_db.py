from db import engine, Base
import models.user
import models.category
import models.transaction

Base.metadata.create_all(engine)