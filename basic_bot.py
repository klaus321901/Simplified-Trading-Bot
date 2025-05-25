import time
import logging
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        self.use_mock = not (api_key and api_secret)
        self.orders = []  # to store placed order details

        if not self.use_mock:
            self.client = Client(api_key, api_secret)
            if testnet:
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            try:
                self.client.futures_account()  # test API validity
                logging.info("Connected to Binance Futures Testnet.")
            except BinanceAPIException as e:
                logging.error(f"API error: {e}")
                self.use_mock = True
                print("API error. Switching to mock mode.")
        else:
            logging.info("Mock mode activated. No API keys provided.")

    # The bot connects to Binance Testnet API if keys are given and valid
    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            if self.use_mock:
                # Simulated response for mock mode
                order = {
                    'success': True,
                    'order_id': int(time.time()),
                    'symbol': symbol,
                    'side': side,
                    'order_type': order_type,
                    'quantity': quantity,
                    'price': price or "market",
                    'stop_price': stop_price,
                    'status': 'filled'
                }
                logging.info(f"[MOCK] Order placed: {order}")
            else:
                if order_type == 'market':
                    order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side.upper(),
                        type='MARKET',
                        quantity=quantity
                    )
                elif order_type == 'limit':
                    order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side.upper(),
                        type='LIMIT',
                        quantity=quantity,
                        price=price,
                        timeInForce='GTC'
                    )
                elif order_type == 'stop_limit':
                    order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side.upper(),
                        type='STOP_MARKET',
                        stopPrice=stop_price,
                        closePosition=False,
                        quantity=quantity,
                        timeInForce='GTC'
                    )
                elif order_type == 'oco':
                    # Simulate OCO: place one limit and one stop order
                    limit_order = {
                        'order_type': 'LIMIT',
                        'price': price,
                        'quantity': quantity
                    }
                    stop_order = {
                        'order_type': 'STOP_MARKET',
                        'stop_price': stop_price,
                        'quantity': quantity
                    }
                    order = {
                        'symbol': symbol,
                        'side': side,
                        'type': 'OCO',
                        'orders': [limit_order, stop_order],
                        'status': 'simulated (OCO not directly supported in futures)'
                    }
                else:
                    return {'success': False, 'error': 'Unsupported order type'}

                logging.info(f"[REAL] Order placed: {order}")

            self.orders.append(order)
            return order

        except BinanceAPIException as e:
            logging.error(f"API exception: {e}")
            return {'success': False, 'error': str(e)}

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {'success': False, 'error': str(e)}

    def view_orders(self):
        return self.orders


# --- Enhanced CLI Interface ---
def menu():
    print("\n Crypto Trading Bot Menu")
    print("1. Place an Order")
    print("2. View Order History")
    print("3. Exit")

def get_order_inputs():
    symbol = input("Enter trading symbol (e.g., BTCUSDT): ").strip().upper()
    side = input("Enter side (BUY/SELL): ").strip().upper()
    order_type = input("Enter order type (market/limit/stop_limit/oco): ").strip().lower()
    quantity = float(input("Enter quantity (e.g., 0.01): ").strip())

    price = None
    stop_price = None

    if order_type in ['limit', 'oco']:
        price = input("Enter limit price: ").strip()

    if order_type in ['stop_limit', 'oco']:
        stop_price = input("Enter stop price: ").strip()

    return symbol, side, order_type, quantity, price, stop_price

if __name__ == "__main__":
    print(" Leave API Key/Secret empty to use mock mode (no real trades).")
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    while True:
        menu()
        choice = input("Select an option (1/2/3): ").strip()

        if choice == '1':
            try:
                symbol, side, order_type, quantity, price, stop_price = get_order_inputs()
                result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
                print("Order Result:", result)
            except Exception as e:
                print(" Error:", e)

        elif choice == '2':
            print("\n Order History:")
            for order in bot.view_orders():
                print(order)

        elif choice == '3':
            print(" Exiting bot.")
            break

        else:
            print(" Invalid choice. Please select 1, 2, or 3.")
