import os
from dotenv import load_dotenv

load_dotenv()


def test_hardcoded_secrets():
    config_vars = {
        'DATABASE_URL': 'default-database-url',
        'DEVELOPMENT_DATABASE_URL': 'default-development-database-url',
        'DEVELOPMENT_RABBITMQ_URI': 'default-rabbitmq-uri',
        'RABBITMQ_URI': 'default-rabbitmq-uri'
    }

    for var, default_value in config_vars.items():
        value = os.getenv(var)
        if value is None:
            print(f"Environment variable {var} is not set")
        elif value == default_value:
            print(
                f"{var} is using a default value, which may indicate a"
                "hardcoded value"
            )
        else:
            print(f"{var} is configured correctly")


def test_suspect_values():
    suspect_values = {
        'default-database-url',
        'localhost',
        'admin',
        'password',
        'test',
        'example'
    }

    config_vars = [
        'DATABASE_URL',
        'DEVELOPMENT_DATABASE_URL',
        'DEVELOPMENT_RABBITMQ_URI',
        'RABBITMQ_URI'
    ]

    for var in config_vars:
        value = os.getenv(var)
        if value is None:
            print(f"Environment variable {var} is not set")
        elif value in suspect_values:
            print(
                f"{var} is using a suspicious value that may be hardcoded"
            )
        else:
            print(
                f"{var} is configured correctly"
            )


test_hardcoded_secrets()
test_suspect_values()
