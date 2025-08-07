from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Bot(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mode = Column(String)  # REAL / SIMULATED
    symbol = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class BotSession(Base):
    __tablename__ = "bot_sessions"
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    pnl = Column(Float, default=0.0)
    grid = Column(JSON, nullable=True)  # 👈 вот здесь правильно!
    bot = relationship("Bot")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("bot_sessions.id"))
    price = Column(Float)
    quantity = Column(Float)
    side = Column(String)  # Buy / Sell
    filled = Column(Float)
    fee = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("BotSession")

class GPTAdvice(Base):
    __tablename__ = "gpt_advice"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("bot_sessions.id"))
    prompt = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship("BotSession")

