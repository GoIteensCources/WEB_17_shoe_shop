from db_settings import Base


base = Base()
base.drop_db()
base.create_db()
