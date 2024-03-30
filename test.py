from lib import Backpack
from config import Config

config = Config()
bp = Backpack(config.get_config()['public_key'], config.get_config()['private_key'])

# Test ping