Feature: Write a REST web service for currency conversion

    Exchange rates might be taken from free sources (e.g. ​https://openexchangerates.org/​) and should be updated once a day. The rates should be stored in a database.
    User interface design is not important and up to you.

    Scenario: Application returns last currency record
        Given server ready to accept requests
        When I request last currency
        Then I have information about cost in Russian Rubles

    Scenario: Data record actually present in database
        Given postgres database
        When I check last currency records in database with SQL
        Then I see table is present
        And I see records

    Scenario: All exchange sources present in api
        Given server ready to accept requests
        When I want to know how much costs <name> with <exchange_code>
        Then I have information about cost in Russian Rubles

        Examples:
            | name          | exchange_code |
            | Czech koruna  | CZK           |
            | Euro          | EUR           |
            | Polish złoty  | PLN           |
            | US dollar     | USD           |
