from lib import Backpack
from config import Config

config = Config()
bp = Backpack(config.get_config()['public_key'], config.get_config()['private_key'])

# Test status
print('Current status:', bp.status())

# Test ping
print('Ping:', bp.ping())

# Test timestamp
print('Timestamp:', bp.time())

# Test get trades
print('Public trades:', bp.get_trades('SOL_USDC'))

# 