from lib import Backpack
from config import Config

# Create a config object to get the public and private keys
config = Config()

# Create a Backpack object
bp = Backpack(config.get_config()['public_key'], config.get_config()['private_key'])

# # Test status
# print('Current status:', bp.status())

# # Test ping
# print('Ping:', bp.ping())

# # Test timestamp
# print('Timestamp:', bp.time())

# # Test get trades
# print('Public trades:', bp.get_trades('SOL_USDC'))

# # Test historical trades
# print('Historical trades:', bp.get_historical_trades('SOL_USDC', 10))

# #Test get assets
# print('Get assets:', bp.get_assets())

# # Test get markets 
# print ('Get markets:', bp.get_markets())

# # Test ticker
# print('Get ticker:', bp.get_ticker('USDT_USDC'))

# #Test get depth
# print('Get depth:', bp.get_depth('SOL_USDC'))

# # Test get klines
# print('Get klines:', bp.get_kline('SOL_USDC', bp.KlineInterval.ONE_MINUTE))

# # Test get account
# print('Get account:', bp.get_balances())

# # Test get deposits
# print('Get deposits:', bp.get_deposits())

# # Test get deposit address
print('Get deposit address:', bp.get_deposit_address(bp.Blockchain.SOLANA))

# Test get orders
# print('Get orders:', bp.get_order_history('SOL_USDC'))