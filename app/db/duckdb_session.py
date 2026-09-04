import duckdb
from app.core.config import settings, PROJECT_ROOT
from app.core.logger import logger

def get_duckdb_connection():
    """
    Returns a DuckDB connection configured to read our parquet files.
    """
    # Use an in-memory DB or a persistent one if configured
    con = duckdb.connect(database=':memory:')
    
    # Create a view that automatically unions all parquet files in the directory
    parquet_path = PROJECT_ROOT / settings.MARKET_DATA_PATH / "*.parquet"
    
    try:
        # Create a view over the parquet files
        # Using string replacement for the path is safe here as it comes from config
        con.execute(f"CREATE OR REPLACE VIEW market_data AS SELECT * FROM read_parquet('{str(parquet_path)}')")
        logger.debug(f"DuckDB initialized with view over {parquet_path}")
    except Exception as e:
        logger.warning(f"Failed to initialize DuckDB view (directory might be empty): {e}")
        
    return con
