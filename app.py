# Iterm
import iterm2
# ccxt async
import ccxt.async_support as ccxt


# Define exchange from this list https://github.com/ccxt/ccxt/wiki/Exchange-Markets
exchange = "binance"
# Define Currency , ex: BTC/USDT
pair = "BTC/USDT"
# Define Update frequency in seconds
updateFrequency = 5

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

# Function that generates a iterm knobs and component, given exchange and pair


def componentGenerator(pair, exchange, updateFrequency):
    key = f"ticker_{exchange}_{pair}"
    knobs = [iterm2.CheckboxKnob(key, False, key)]
    component = iterm2.StatusBarComponent(
        short_description=key,
        detailed_description="Crypto Ticker Component, supporting over 100 exchanges and 1000 coins",
        knobs=knobs,
        exemplar="BTC $1",
        update_cadence=updateFrequency,
        identifier=f"com.iterm2.example.{key}")
    return knobs, component


async def main(connection):
    global pair
    global exchange
    global updateFrequency

    knobs, component = componentGenerator(pair, exchange, updateFrequency)

    @iterm2.StatusBarRPC
    async def tickerUpdate(
            knobs,
    ):
        price = await get_price(pair)
        return f"{pair} ${price}"

    # Register the component.
    await component.async_register(connection, tickerUpdate)

iterm2.run_forever(main)
