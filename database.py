from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://neondb_owner:npg_W7BH8wZTNRPQ@ep-wispy-bread-a48gu1mq-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require'

engine = create_engine(URL_DATABASE);

Session = sessionmaker(autoflush=False, bind=engine);

Base = declarative_base()