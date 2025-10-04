import configparser
import os

# Ensure the config.ini file exists in the expected location
config_file_path = 'config.ini'
if not os.path.exists(config_file_path):
    raise FileNotFoundError(f"The config file '{config_file_path}' was not found.")

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the configuration file
config.read(config_file_path)

# Check if the sections exist before accessing them
if 'jwt' not in config:
    raise KeyError("Section 'jwt' not found in the configuration file.")

if 'database' not in config:
    raise KeyError("Section 'database' not found in the configuration file.")

if 'oauth2' not in config:
    raise KeyError("Section 'oauth2' not found in the configuration file.")

JWT_SECRET_KEY = config['jwt']['secret_key']
JWT_ALGORITHM = config['jwt']['algorithm']
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config.getint('jwt', 'access_token_expire_minutes')
DB_URL = config['database']['db_url']
TOKEN_URL = config['oauth2']['token_url']
