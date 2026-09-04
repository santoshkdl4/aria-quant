from app.db.session import MemorySessionLocal
from app.db.models_memory import Strategy, Experiment
from sqlalchemy.orm import Session
from app.core.logger import logger

class MemoryManager:
    @staticmethod
    def save_strategy_evaluation(
        experiment_id: int, 
        name: str, 
        code: str, 
        metrics: dict, 
        status: str,
        failure_reason: str = ""
    ):
        db: Session = MemorySessionLocal()
        try:
            strategy = Strategy(
                experiment_id=experiment_id,
                name=name,
                description=f"Generated via experiment {experiment_id}",
                code_snippet=code,
                status=status, # 'PROMOTED' or 'REJECTED'
                performance_metrics=metrics,
                failure_reason=failure_reason
            )
            db.add(strategy)
            db.commit()
            db.refresh(strategy)
            logger.info(f"Saved strategy {name} as {status} to Graveyard/Memory")
            return strategy
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save strategy: {e}")
        finally:
            db.close()
            
    @staticmethod
    def get_graveyard_summary():
        db: Session = MemorySessionLocal()
        try:
            strategies = db.query(Strategy).filter(Strategy.status == 'REJECTED').all()
            return [
                {
                    "name": s.name, 
                    "reason": s.failure_reason, 
                    "metrics": s.performance_metrics
                } for s in strategies
            ]
        finally:
            db.close()
            
    @staticmethod
    def create_experiment(agent_id: str, prompt: str) -> int:
        db: Session = MemorySessionLocal()
        try:
            exp = Experiment(agent_id=agent_id, prompt_used=prompt)
            db.add(exp)
            db.commit()
            db.refresh(exp)
            return exp.id
        finally:
            db.close()
