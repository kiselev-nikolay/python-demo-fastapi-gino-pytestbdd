import asyncio

from server.integrations import openexchangerates
from server.models.repository import Currency


async def start_refresh_rates_routine():
    asyncio.create_task(_refresh_rates_routine())


async def _refresh_rates_routine(delay=False):
    if delay:
        await asyncio.sleep(60 * 60 * 24)
    asyncio.create_task(_refresh_rates_routine(delay=True))
    await refresh_rates()


async def refresh_rates():
    currencies = await openexchangerates.decimals()
    for currency_name, currency_rate in currencies.items():
        cur = await Currency.query.where(Currency.exchange_code == currency_name).gino.first()
        if cur:
            await cur.update(rate=currency_rate).apply()
        else:
            await Currency.create(exchange_code=currency_name, rate=currency_rate)
