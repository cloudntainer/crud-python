import logging
from urllib.parse import urlparse, ParseResult
from config.config import Config

logger = logging.getLogger(__name__)


def parse_database_url():
    """
    Parses the database URL from configuration and returns a dictionary.

    Returns:
        dict: A dictionary containing database connection parameters.

    Raises:
        ValueError: If DATABASE_URL is not configured or is invalid.
    """
    url = Config.DATABASE_URL
    if not url:
        logger.error("DATABASE_URL is not configured.")
        raise ValueError("DATABASE_URL is not configured.")

    try:
        parsed_url: ParseResult = urlparse(url)
    except Exception as e:
        logger.error(f"Error parsing DATABASE_URL: {e}")
        raise ValueError(f"Error parsing DATABASE_URL: {e}")

    db_info = {
        'dbname': parsed_url.path[1:],
        'user': parsed_url.username,
        'password': parsed_url.password,
        'host': parsed_url.hostname,
        'port': parsed_url.port
    }

    for key, value in db_info.items():
        if value is None:
            logger.error(f"{key} is missing in DATABASE_URL.")
            raise ValueError(f"{key} is missing in DATABASE_URL.")

    return db_info
