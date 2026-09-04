import os
import glob
from pathlib import Path
import duckdb
from loguru import logger
from app.core.config import settings, APP_DATA_DIR

def ingest_legacy_csv_data(source_dir: str):
    """
    Scans the given source directory for CSV files (excluding .venv) and converts
    them to highly optimized Parquet files inside ARIA's data vault.
    """
    logger.info(f"Starting data ingestion from: {source_dir}")
    source_path = Path(source_dir)
    
    if not source_path.exists() or not source_path.is_dir():
        logger.error(f"Source directory {source_dir} does not exist.")
        return False
        
    target_data_dir = APP_DATA_DIR / settings.MARKET_DATA_PATH
    target_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize DuckDB connection for processing
    con = duckdb.connect(database=':memory:')
    
    # Find all CSV files recursively using glob
    csv_files = []
    for root, dirs, files in os.walk(source_dir):
        # Skip .venv and other hidden/system folders
        if '.venv' in root or '.git' in root:
            continue
        for f in files:
            if f.endswith('.csv'):
                csv_files.append(os.path.join(root, f))
                
    if not csv_files:
        logger.warning(f"No CSV files found in {source_dir}")
        return True
        
    logger.info(f"Found {len(csv_files)} CSV files. Beginning conversion to Parquet...")
    
    success_count = 0
    error_count = 0
    
    for csv_file in csv_files:
        try:
            rel_path = os.path.relpath(csv_file, source_dir)
            # Create a target path replacing .csv with .parquet
            # Recreate the tree for better organization.
            target_rel_path = Path(rel_path).with_suffix('.parquet')
            target_file = target_data_dir / target_rel_path
            
            # Ensure target subdirectories exist
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Use DuckDB to efficiently read the CSV and write to Parquet
            # read_csv_auto automatically detects headers and data types
            query = f"""
                COPY (SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=true)) 
                TO '{str(target_file)}' (FORMAT PARQUET, COMPRESSION 'ZSTD');
            """
            con.execute(query)
            success_count += 1
            logger.debug(f"Successfully converted {rel_path}")
        except Exception as e:
            error_count += 1
            logger.error(f"Failed to convert {csv_file}: {e}")
            
    logger.info(f"Ingestion complete. Successfully converted: {success_count}, Errors: {error_count}")
    return True

if __name__ == "__main__":
    # Test script execution
    # Legacy path provided by the user
    legacy_path = r"E:\001 ChatGPT_Projects\AI Trading Bot FnO"
    ingest_legacy_csv_data(legacy_path)
