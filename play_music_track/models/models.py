from sqlalchemy import Column, Integer, String
from database import Base


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    track_name = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
