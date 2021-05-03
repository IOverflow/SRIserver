from dependencies.dbconnection import Base, engine

def load_database():
    Base.metadata.create_all(bind=engine)