import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_env_variable(var_name, default=None):
    """Gets the environment variable or raises an error if not found."""
    value = os.getenv(var_name, default)
    if value is None and default is None:
        logger.error(f"Missing environment variable '{var_name}'.")
        raise EnvironmentError(f"Missing environment variable: {var_name}")
    return value


class Config:
    """Configuration class for the application."""
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']

    # DATABASE_URL = get_env_variable('DATABASE_URL')  # Commented out
    # SECRET_KEY = get_env_variable('SECRET_KEY')      # Commented out

    @classmethod
    def validate(cls):
        """Validates required environment variables."""
        # required_vars = ['DATABASE_URL', 'SECRET_KEY']  # Commented out

        # Check for any required environment variables
        # missing_vars = [var for var in required_vars if not os.getenv(var)]

        # if missing_vars:
        #     logger.error(
        #         "Missing environment variables: %s", ', '.join(missing_vars)
        #     )
        #     raise EnvironmentError(
        #         "Required environment variables are missing: "
        #         f"{', '.join(missing_vars)}"
        #     )

        logger.info("All required environment variables are present.")


if __name__ == "__main__":
    Config.validate()
