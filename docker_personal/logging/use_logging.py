from centralized_logging import setup_logger

# Initialize logger
logger = setup_logger("Script2Logger")

logger.info("Script 2 is running smoothly")
logger.warning("Low memory warning in script 2")
logger.error("Critical error in script 2!")
