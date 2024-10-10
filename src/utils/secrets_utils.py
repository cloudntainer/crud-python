import logging

logger = logging.getLogger(__name__)


def validate_secrets(config):
    """
    Validates that all required environment variables are configured.
    Returns a dictionary of the required environment variables.
    Raises ValueError if any variable is missing.
    """
    required_secrets = {
        'POSTGRES_DB': config.POSTGRES_DB,
        'POSTGRES_USER': config.POSTGRES_USER,
        'POSTGRES_PASSWORD': config.POSTGRES_PASSWORD,
        'RABBITMQ_URI': config.RABBITMQ_URI
    }

    missing_vars = [var for var, value in required_secrets.items() if value is None]

    if missing_vars:
        missing_vars_str = ', '.join(missing_vars)
        logger.error(f"The following environment variables are missing: {missing_vars_str}")
        raise ValueError(f"Required environment variables are missing: {missing_vars_str}")

    logger.info("All required environment variables are present.")
    return required_secrets
