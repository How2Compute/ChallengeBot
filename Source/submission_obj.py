from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

# ORM object for a submission
class Submission(Base):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    challange_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String(250), nullable=False)
    notes = Column(String(250), nullable=False)

    # Default Constructor (using notes = None/"None" to allow noteless submissions)
    def __init__(self, challange_id, user_id, url, notes = "None"):
        self.user_id = user_id
        self.url = url
        self.challange_id = challange_id
        self.notes = notes
