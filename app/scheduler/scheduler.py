from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.logger import logger
from datetime import datetime

scheduler = AsyncIOScheduler()

def job_eod_data_ingestion():
    logger.info(f"[{datetime.now()}] Triggered Scheduled Job: EOD Data Ingestion")
    # In production, this would call fetchers.py for all tracked universe symbols.

def job_overnight_research():
    logger.info(f"[{datetime.now()}] Triggered Scheduled Job: Overnight AI Research")
    # In production, this wakes up the ResearchAgent

def job_intraday_paper_trading():
    logger.info(f"[{datetime.now()}] Triggered Scheduled Job: Intraday Paper Trading")
    # In production, this triggers the executor.py to scan for signals

def start_scheduler():
    logger.info("Starting ARIA Job Scheduler...")
    
    # EOD Data (e.g., 4:00 PM IST)
    scheduler.add_job(job_eod_data_ingestion, 'cron', hour=16, minute=0)
    
    # Overnight Research (e.g., 11:00 PM IST)
    scheduler.add_job(job_overnight_research, 'cron', hour=23, minute=0)
    
    # Intraday Check (e.g., Every 15 mins)
    scheduler.add_job(job_intraday_paper_trading, 'interval', minutes=15)
    
    scheduler.start()

def stop_scheduler():
    logger.info("Stopping ARIA Job Scheduler...")
    scheduler.shutdown()
