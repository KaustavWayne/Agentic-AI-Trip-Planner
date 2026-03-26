# logging configuration
import logging 
from pathlib import Path 

def setup_logger(name: str = "trip_planner"): 
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    handler = logging.FileHandler(log_dir / "trip_planner.log")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)
    return logger 

logger = setup_logger()