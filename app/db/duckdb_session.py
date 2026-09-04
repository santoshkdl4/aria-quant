import duckdb
from app.core.config import settings, APP_DATA_DIR
from app.core.logger import logger

def get_duckdb_connection():
    """
    Returns a DuckDB connection configured to read our parquet files.
    """
    # Use an in-memory DB or a persistent one if configured
    con = duckdb.connect(database=':memory:')
    
    # Create a view that automatically unions all parquet files in the directory recursively
    # Explicitly require 'symbol=' to prevent loading backtest results or unpartitioned data
    parquet_path = APP_DATA_DIR / settings.MARKET_DATA_PATH / "symbol=*" / "**" / "*.parquet"
    
    try:
        # Create a view over the parquet files with hive partitioning enabled
        # Using string replacement for the path is safe here as it comes from config
        # Convert path to posix for DuckDB globbing compatibility
        posix_path = str(parquet_path).replace("\\", "/")
        con.execute(f"CREATE OR REPLACE VIEW market_data AS SELECT * FROM read_parquet('{posix_path}', hive_partitioning=1)")
        logger.debug(f"DuckDB initialized with Hive view over {posix_path}")
    except Exception as e:
        logger.warning(f"Failed to initialize DuckDB Hive view (directory might be empty): {e}")
        
    return con
