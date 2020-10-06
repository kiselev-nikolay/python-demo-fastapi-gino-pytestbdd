import cachetools
import httpx

BASE_URL = "https://openexchangerates.org"
APP_ID = "a2d841b648df49efb764a5f74ccb48e0"
BASE_CUR = "RUB"

_CACHE = cachetools.TTLCache(12, 60)


async def raw_request():
    try:  # EAFP thing
        return _CACHE["raw_request"]
    except LookupError:
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            resp = await client.get(
                "/api/latest.json",
                params=dict(
                    app_id=APP_ID,
                    # base=BASE
                ),
            )
        # API does not provide a free base currency change. So we convert manually.
        data = resp.json()
        base_cur = data["rates"][BASE_CUR]
        data["base"] = BASE_CUR
        for cur in data["rates"]:
            data["rates"][cur] = data["rates"][cur] / base_cur
        _CACHE["raw_request"] = data
        return _CACHE["raw_request"]


async def decimals():
    data = await raw_request()
    return {k: round(v, 2) for k, v in data["rates"].items()}
