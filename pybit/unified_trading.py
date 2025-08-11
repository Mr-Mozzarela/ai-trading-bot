class HTTP:
    """Minimal stub for pybit.unified_trading.HTTP."""
    def __init__(self, api_key=None, api_secret=None, testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

    def get_wallet_balance(self, accountType=None):
        """Return a fake USDT balance."""
        return {
            "result": {
                "list": [
                    {"coin": [{"coin": "USDT", "walletBalance": "1000"}]}
                ]
            }
        }

    def get_tickers(self, category, symbol):
        """Return a static price and volume for any symbol."""
        return {
            "result": {
                "list": [
                    {"lastPrice": "30000", "turnover24h": "1000000"}
                ]
            }
        }

    def get_instruments_info(self, category, symbol):
        """Minimal instrument info used in tests."""
        return {
            "result": {
                "list": [
                    {
                        "lotSizeFilter": {"minOrderQty": "0.001"},
                        "priceFilter": {"tickSize": "0.5"},
                    }
                ]
            }
        }

    def place_order(self, **kwargs):
        return {"result": "order placed", "input": kwargs}

    def cancel_all_orders(self, **kwargs):
        return {"result": "orders cancelled", "input": kwargs}
