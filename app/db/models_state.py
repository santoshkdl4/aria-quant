from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class AgentState(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True) # Unique agent ID
    role = Column(String, index=True)
    status = Column(String, default="IDLE") # IDLE, RESEARCHING, WAITING
    current_task = Column(String, nullable=True)
    parent_id = Column(String, nullable=True)
    model = Column(String, nullable=True)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

class ApprovalRequest(Base):
    __tablename__ = "approvals"

    id = Column(String, primary_key=True, index=True)
    requester = Column(String) # Agent ID
    action = Column(String)
    reason = Column(String)
    cost_estimate = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

class PortfolioState(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    virtual_capital = Column(Float, default=1000000.0)
    current_portfolio_value = Column(Float, default=1000000.0)
    active_positions = Column(JSON, default=dict)
    trade_history = Column(JSON, default=list)
