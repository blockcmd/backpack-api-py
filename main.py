from lib import Backpack
from config import Config

# Create a config object to get the public and private keys
config = Config()

# Create a Backpack object
bp = Backpack(config.get_config()['public_key'], config.get_config()['private_key'])