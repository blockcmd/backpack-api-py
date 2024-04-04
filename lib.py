import requests
import json
from enum import Enum
from time import time
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

class Backpack:

    class KlineInterval(Enum):
        ONE_MINUTE = '1m'
        THREE_MINUTES = '3m'
        FIVE_MINUTES = '5m'
        FIFTEEN_MINUTES = '15m'
        THIRTY_MINUTES = '30m'
        ONE_HOUR = '1h'
        TWO_HOURS = '2h'
        FOUR_HOURS = '4h'
        SIX_HOURS = '6h'
        EIGHT_HOURS = '8h'
        TWELVE_HOURS = '12h'
        ONE_DAY = '1d'
        THREE_DAYS = '3d'
        ONE_WEEK = '1w'
        ONE_MONTH = '1month'

    class Blockchain(Enum):
        ETHEREUM = 'Ethereum'
        SOLANA = 'Solana'
        POLYGON = 'Polygon'
        BITCOIN = 'Bitcoin'

    class OrderType(Enum):
        LIMIT = 'Limit'
        MARKET = 'Market'

    class SelfTradePrevention(Enum):
        REJECT_TAKER = 'RejectTaker'
        REJECT_MAKER = 'RejectMaker'
        REJECT_BOTH = 'RejectBoth'
        ALLOW = 'Allow'

    class Side(Enum): 
        BID = 'Bid'
        ASK = 'Ask'

    class TimeInForce(Enum):
        GTC = 'GTC'
        IOC = 'IOC'
        FOK = 'FOK'


    def __init__(self, public_key: str, private_key: str):
        self.__public_key = public_key
        self.__private_key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(private_key))


    def __header(self):
        header = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'
        }
        return header
    

    def __header_private(self, timestamp: int, signature: str, window: int = 5000):
        header = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-API-KEY': self.__public_key,
            'X-Signature': signature,
            'X-Timestamp': str(timestamp),
            'X-Window': str(window)
        }
        return header


    def __get(self, request_path, params=''):
        base_url = 'https://api.backpack.exchange/'
        url = base_url + request_path + params
        header = self.__header()
        response = requests.get(url, headers=header)
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text


    def __signature(self, timestamp: int, instruction: str, params: str = '', body: dict = None):
        # order params alphabetically
        if params != '':
            sorted_params = params.split('&')[1:]
            sorted_params.sort()
            sorted_params = '&' + '&'.join(sorted_params)
        else:
            sorted_params = ''
        
        if body:
            body_to_params = ''
            for key, value in body.items():  # Iterate over items of the body dictionary
                body_to_params += f'&{key}={value}'
            body_to_params = body_to_params.split('&')[1:]
            body_to_params.sort()
            sorted_string = '&' + '&'.join(body_to_params)
        else:
            sorted_string = ''
        completed_params = f'instruction={instruction}' + sorted_params + sorted_string + f'&timestamp={timestamp}&window=5000'
        raw_signature = self.__private_key.sign(completed_params.encode())
        signature = base64.b64encode(raw_signature).decode()
        return signature


    def __get_private(self, request_path: str, instruction: str, params: str = '', body: dict = {}):
        base_url = 'https://api.backpack.exchange/'
        url = base_url + request_path + f'?instruction={instruction}' + params
        timestamp = int(time() * 1000)
        signature = self.__signature(timestamp, instruction, params)
        header = self.__header_private(timestamp, signature)
        response = requests.get(url, headers=header, data=body)
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
        
        
    def __post(self, request_path: str, instruction: str, params: str = '', body: dict = None):
        base_url = 'https://api.backpack.exchange/'
        url = base_url + request_path + f'?instruction={instruction}' + params
        timestamp = int(time() * 1000)
        signature = self.__signature(timestamp, instruction, params, body)
        header = self.__header_private(timestamp, signature)
        response = requests.post(url, headers=header, data=json.dumps(body))
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
        

    def __delete(self, request_path: str, instruction: str, params: str = '', body: dict = None):
        base_url = 'https://api.backpack.exchange/'
        url = base_url + request_path + f'?instruction={instruction}' + params
        timestamp = int(time() * 1000)
        signature = self.__signature(timestamp, instruction, params, body)
        header = self.__header_private(timestamp, signature)
        response = requests.delete(url, headers=header, data=json.dumps(body))
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text    


    def status(self):
        """
        Get the current status of the platform.
        Returns:
            The status of the platform.
        """
        return self.__get('api/v1/status')

    
    def ping(self):
        """
        Ping the platform to receive a pong
        Returns:
            A pong from the platform.
        """
        return self.__get('api/v1/ping')
    

    def time(self):
        """
        Get the current time of the platform.
        Returns:
            The current time of the platform.
        """
        return self.__get('api/v1/time')
    

    def get_trades(self, symbol: str, limit: int = 100):
        """
        Get the trades for a specific symbol.
        Args:
            symbol (str): The symbol to retrieve trades for. (Required)
            limit (int): The maximum number of trades to retrieve. Default is 100; max is 1000. (Optional)
        Returns:
            The trades for the specified symbol.
        """
        return self.__get('api/v1/trades', f'?symbol={symbol}&limit={limit}')
    

    def get_historical_trades(self, symbol: str, limit: int = 100, offset: int = 0):
        """
        Get the historical trades for a specific symbol.
        Args:
            symbol (str): The symbol to retrieve historical trades for. (Required)
            limit (int): Limit the number of trades returned. Default 100, maximum 1000. (Optional)
            offset (int): The starting point for the historical trades. Default is 0. (Optional)
        Returns:
            The historical trades for the specified symbol.
        """
        return self.__get('api/v1/trades/history', f'?symbol={symbol}&limit={limit}&offset={offset}')


    def get_assets(self):
        """
        Get all the assets that are supported by the exchange.
        Returns:
            All the assets that are supported by the exchange.
        """
        return self.__get('api/v1/assets')
    

    def get_markets(self):
        """
        Get all the markets that are supported by the exchange.
        Returns:
            All the markets that are supported by the exchange.
        """
        return self.__get('api/v1/markets')


    def get_ticker(self, symbol: str):
        """
        Get the ticker for a specific symbol.
        Args:
            symbol (str): The symbol to retrieve the ticker for. (Required)
        Returns:
            The ticker for the specified symbol.
        """
        return self.__get('api/v1/ticker', f'?symbol={symbol}')


    def get_tickers(self):
        """
        Get summarised statistics for the last 24 hours for all market symbols..
        Returns:
            Summarised statistics for the last 24 hours for all market symbols..
        """
        return self.__get('api/v1/tickers')


    def get_depth(self, symbol: str):
        """
        Get the order book for a specific symbol.
        Args:
            symbol (str): The symbol to retrieve the order book for. (Required)
        Returns:
            The order book for the specified symbol.
        """
        return self.__get('api/v1/depth', f'?symbol={symbol}')
    

    def get_kline(self, symbol: str, interval: KlineInterval):
        """
        Get the kline for a specific symbol.
        Args:
            symbol (str): The symbol to retrieve the kline for. (Required)
            interval (str): The interval for the kline. (Required)
            limit (int): The maximum number of kline to retrieve. Default is 100; max is 1000. (Optional)
        Returns:
            The kline for the specified symbol.
        """
        return self.__get('api/v1/klines', f'?symbol={symbol}&interval={interval.value}')
    

    def get_balances(self):
        """
        Get the balances for the authenticated user.
        Returns:
            The balances for the authenticated user.
        """
        return self.__get_private('api/v1/capital', 'balanceQuery')
    
    
    def get_deposits(self, limit: int = 100, offset: int = 0):
        """
        Get the deposits for the authenticated user.
        Args:
            limit (int): Limit the number of deposits returned. Default 100, maximum 1000. (Optional)
            offset (int): The starting point for the deposits. Default is 0. (Optional)
        Returns:
            The deposits for the authenticated user.
        """
        return self.__get_private('wapi/v1/capital/deposits', 'depositQueryAll', f'&limit={limit}&offset={offset}')
    
    
    def get_deposit_address(self, blockchain: Blockchain):
        """
        Get the deposit address for the authenticated user.
        Args:
            blockchain (str): The blockchain to retrieve the deposit address for. (Required)
        Returns:
            The deposit address for the authenticated user.
        """
        return self.__get_private('wapi/v1/capital/deposit/address', 'depositAddressQuery', f'&blockchain={blockchain.value}')
    

    def get_withdrawals(self, limit: int = 100, offset: int = 0):
        """
        Get the withdrawals for the authenticated user.
        Args:
            limit (int): Limit the number of withdrawals returned. Default 100, maximum 1000. (Optional)
            offset (int): The starting point for the withdrawals. Default is 0. (Optional)
        Returns:
            The withdrawals for the authenticated user.
        """
        return self.__get_private('wapi/v1/capital/withdrawals', 'withdrawalQueryAll', f'&limit={limit}&offset={offset}')
    

    def get_order_history(self, orderId: str, symbol: str, limit: int = 100, offset: int = 0):
        """
        Get the orders for the authenticated user.
        Args:
            orderId (str): The order id to retrieve. (Required)
            symbol (str): The symbol to retrieve the orders for. (Required)
            limit (int): Limit the number of orders returned. Default 100, maximum 1000. (Optional)
            offset (int): The starting point for the orders. Default is 0. (Optional)
        Returns:
            The orders for the authenticated user.
        """
        return self.__get_private('wapi/v1/history/orders', 'orderHistoryQueryAll', f'&limit={limit}&offset={offset}&orderId={orderId}&symbol={symbol}&limit={limit}&offset={offset}')
    

    def get_fill_history(self, orderId: str, _from: int, _to: int, symbol: str, limit: int = 100, offset: int = 0):
        """
        Get the fills for the authenticated user.
        Args:
            symbol (str): The symbol to retrieve the fills for. (Required)
            limit (int): Limit the number of fills returned. Default 100, maximum 1000. (Optional)
            offset (int): The starting point for the fills. Default is 0. (Optional)
        Returns:
            The fills for the authenticated user.
        """
        return self.__get_private('wapi/v1/history/fills', 'fillHistoryQueryAll', f'&symbol={symbol}&limit={limit}&offset={offset}')
    

    def create_order(self, orderType: OrderType, price: str, quantity: str, side: Side, symbol: str, timeInForce: TimeInForce = None, triggerPrice: str = None, quoteQuantity: str = None, clientId: int = None, postOnly: str = None, selfTradePrevention: SelfTradePrevention = None):
        """
        Create an order for the authenticated user.
        Args:
            orderType (str): The type of order to create. (Required)
            postOnly (str): Post only flag. (Required)
            price (str): The price of the order. (Required)
            quantity (str): The quantity of the order. (Required)
            selfTradePrevention (str): Self trade prevention flag. (Required)
            side (str): The side of the order. (Required)
            symbol (str): The symbol to create the order for. (Required)
            timeInForce (str): The time in force of the order. (Required)
            triggerPrice (str): The trigger price of the order. (Required)
            quoteQuantity (str): The quote quantity of the order. (Optional)
            clientId (int): The client id of the order. (Optional)
        Returns:
            The order for the authenticated user.
        """
        # construct order data, if input is not None
        order_data = {
            'orderType': orderType.value,
            'price': price,
            'quantity': quantity,
            'side': side.value,
            'symbol': symbol,
        }

        if timeInForce:
            order_data['timeInForce'] = timeInForce
        if triggerPrice:
            order_data['triggerPrice'] = triggerPrice
        if quoteQuantity:
            order_data['quoteQuantity'] = quoteQuantity
        if clientId:
            order_data['clientId'] = clientId
        if postOnly:
            order_data['postOnly'] = postOnly
        if selfTradePrevention:
            order_data['selfTradePrevention'] = selfTradePrevention.value

        print(order_data)
        return self.__post(request_path='api/v1/order', instruction='orderExecute', body=order_data)