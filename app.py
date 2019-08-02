# Iterm
import iterm2
# ccxt async
import ccxt.async_support as ccxt


# Define exchange from this list https://github.com/ccxt/ccxt/wiki/Exchange-Markets
exchange = "binance"
# Define Currency , ex: BTC/USDT
pair = "BTC/USDT"


# Initialize exchange interface
exchIface = getattr(ccxt, exchange)()


# Function to get price using exchIface
async def get_price(pair):
    global exchIface

    try:
        # Get ticker
        ticker = await exchIface.fetchTicker(pair)
        # Get the price
        price = ticker.get('last', "Error")
        # Format the price
        result = f"{price:,.2f}"
    except Exception as e:
        # Print exception for debugging
        print(e)
        # Set exception as result
        result = str(e)

    return result


async def main(connection):
    global pair
    # Define the configuration knobs:
    vl = "crypto_ticker"
    knobs = [iterm2.CheckboxKnob("Crypto Ticker", False, vl)]
    component = iterm2.StatusBarComponent(
        short_description="Crypto Ticker",
        detailed_description="Crypto Ticker Component, supporting over 100 exchanges and 1000 coins",
        knobs=knobs,
        exemplar="BTC $100,000",
        update_cadence=5,
        identifier="com.iterm2.example.btc-ticker")

    # This function gets called whenever any of the paths named in defaults (below) changes
    # or its configuration changes.
    # References specify paths to external variables (like rows) and binds them to
    # arguments to the registered function (coro). When any of those variables' values
    # change the function gets called.
    @iterm2.StatusBarRPC
    async def coro(
            knobs,
    ):
        price = await get_price(pair)
        return f"{pair} ${price}"

    # Register the component.
    await component.async_register(connection, coro)

iterm2.run_forever(main)
