from database.dao import engine, Base

Base.metadata.create_all(engine)