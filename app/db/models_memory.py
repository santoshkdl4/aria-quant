from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, index=True) # e.g. EXP-000001
    title = Column(String)
    hypothesis = Column(String)
    agent_id = Column(String)
    market = Column(String)
    status = Column(String, default="IDEA") # IDEA, INITIAL_TEST, VALIDATING, REJECTED, APPROVED
    parameters = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    lessons_learned = Column(String, nullable=True)

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(String, primary_key=True, index=True) # e.g. STRAT-001
    name = Column(String)
    experiment_id = Column(String, ForeignKey("experiments.id"))
    status = Column(String, default="RESEARCHING") # RESEARCHING, PAPER_TRADING, REJECTED, ARCHIVED
    rejection_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DecisionLog(Base):
    __tablename__ = "decision_log"

    id = Column(String, primary_key=True, index=True) # e.g. DEC-0001
    decision = Column(String)
    alternatives_considered = Column(String)
    reason = Column(String)
    consequences = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemMemory(Base):
    __tablename__ = "system_memory"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True) # market, strategy, system, operational
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
