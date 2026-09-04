import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.db.models_state import AgentState
from app.db.models_memory import Experiment

@pytest.fixture
def test_state_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def test_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_agent_state(test_state_db):
    agent = AgentState(id="agent-001", role="Master Trader", status="IDLE")
    test_state_db.add(agent)
    test_state_db.commit()
    
    fetched = test_state_db.query(AgentState).filter_by(id="agent-001").first()
    assert fetched is not None
    assert fetched.role == "Master Trader"

def test_create_experiment(test_memory_db):
    exp = Experiment(id="EXP-001", title="Test Hypothesis", status="IDEA")
    test_memory_db.add(exp)
    test_memory_db.commit()
    
    fetched = test_memory_db.query(Experiment).filter_by(id="EXP-001").first()
    assert fetched is not None
    assert fetched.title == "Test Hypothesis"
