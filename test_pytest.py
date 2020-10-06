import asyncio
import logging
from time import sleep

import pytest
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from pytest_bdd import given, scenario, then, when

from alembic.config import main
from server.app import app, db
from server.models.settings import Settings
from server.startup import refresh_rates

pytest_plugins = ["docker_compose"]


@pytest.fixture
def database(session_scoped_container_getter):
    del session_scoped_container_getter
    for _ in range(100):
        try:
            main(["--raiseerr", "upgrade", "head"])
            break
        except Exception as e:
            logging.error(e)
            sleep(0.5)
    else:
        raise ConnectionError("Cannot connect to pg.")
    asyncio.get_event_loop().run_until_complete(db.set_bind(Settings().pg_dsn))
    yield db


@pytest.fixture
def client(database):
    asyncio.get_event_loop().run_until_complete(refresh_rates())
    with TestClient(app) as client:
        yield client


@scenario("features/webservice.feature", "All exchange sources present in api")
def test_all_exchange_sources_present_in_api():
    """All exchange sources present in api."""


@scenario("features/webservice.feature", "Application returns last currency record")
def test_application_returns_last_currency_record():
    """Application returns last currency record."""


@scenario("features/webservice.feature", "Data record actually present in database")
def test_data_record_actually_present_in_database():
    """Data record actually present in database."""


@given("postgres database")
def postgres_database(database):
    """postgres database."""
    del database


@given("server ready to accept requests")
def server_ready_to_accept_requests(client):
    """server ready to accept requests."""
    del client


@when("I check last currency records in database with SQL")
def i_check_last_currency_records_in_database_with_sql(database):
    """I check last currency records in database with SQL."""
    assert "currency" in database.tables


@when("I request last currency")
def i_request_last_currency(client):
    """I request last currency."""
    currencies_resp = client.get("/api/v1/currencies")
    currencies_resp.raise_for_status()
    currencies = currencies_resp.json()
    assert currencies["success"]
    assert currencies["result"]["rates"]


@when("I want to know how much costs <name> with <exchange_code>")
def i_want_to_know_how_much_costs_name_with_exchange_code(client, exchange_code):
    """I want to know how much costs <name> with <exchange_code>."""
    currency_resp = client.get("/api/v1/currency/" + exchange_code)
    currency_resp.raise_for_status()
    currency = currency_resp.json()
    assert currency["success"]
    assert currency


@then("I have information about cost in Russian Rubles")
def i_have_information_about_cost_in_russian_rubles():
    """I have information about cost in Russian Rubles."""


@then("I see records")
def i_see_records():
    """I see records."""


@then("I see table is present")
def i_see_table_is_present():
    """I see table is present."""
