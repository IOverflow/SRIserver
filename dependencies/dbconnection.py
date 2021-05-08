import databases
from sqlalchemy.sql.schema import MetaData
from config import settings
import sqlalchemy
from databases import Database

database: Database = Database(settings.DATABASE_URL)

metadata: MetaData = sqlalchemy.MetaData()