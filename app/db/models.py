from sqlalchemy import Column, String, DateTime, Integer, Float, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Call(Base):
    __tablename__ = "calls"

    call_id = Column(String, primary_key=True)
    agent_id = Column(String, index=True)
    customer_id = Column(String)
    language = Column(String)
    start_time = Column(DateTime, index=True)
    duration_seconds = Column(Integer)
    transcript = Column(Text)
    agent_talk_ratio = Column(Float)
    customer_sentiment_score = Column(Float)
    embedding = Column(Text)

    __table_args__ = (
        Index("ix_calls_transcript_gin", "transcript", postgresql_using="gin"),
    )
