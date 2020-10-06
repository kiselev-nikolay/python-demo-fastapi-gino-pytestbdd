from fastapi import APIRouter

from server.models.repository import Currency
from server.models.responses import NotFound, Success

router = APIRouter()


@router.get("/currencies")
async def all():
    currencies = await Currency.query.gino.all()
    response = [cur.to_dict() for cur in currencies]
    return Success(result={"rates": response})


@router.get("/currency/{exchange_code}")
async def by_exchange_code(exchange_code: str):
    currency = await Currency.query.where(Currency.exchange_code == exchange_code.upper()).gino.first()
    if currency:
        return Success(result=currency.to_dict())
    else:
        return NotFound()
