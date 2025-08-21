from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base


class Message(Base):
    __tablename__ = "fct_messages"
    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    message_text = Column(String)
    posted_at = Column(DateTime)
    

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    id = Column(Integer, primary_key=True, index=True)
    detected_object_class = Column(String)
    confidence_score = Column(Float)
    detected_at = Column(DateTime)
