# Introduction

This is homework for two services -  event propagator and event consumer. Propagator is python script, consumer is FastApi app.
Uses environment variables so safe for containerization.
Dependancies and environment managed by poetry.
Petry.lock is present so `make install` will setup environment.
Requires two terminals.
Tested on WSL.

# Configuration

1. For propagator - `propagator/configuration/.env-propagator`

    1.1 PERIOD_SECONDS - How often to send event

    1.2 CONSUMER_ENDPOINT - Where to send event

    1.3 EVENTS_FILE - Where to read events from file path

2. For consumer - `consumer/configuration/.env-consumer`

    2.1 CONSUMER_PORT - Fastapi port to run on localhost

    2.2 STORAGE_TYPE - Saving events. Possible values: DB , FILE

    2.3 STORAGE_FILE - Saving events. File .log location

    2.4 DB_URL - Saving events. File .db location

# Steps to launch

1. locate where Makefile is located
2. `make install`
3. `run-consumer`
4. open another terminal window - run command `run-propagator`
5. (Optional) `run-tests` - added one test due to time constrains

# Flow

1. Propagator sends every `PERIOD_SECONDS` event read from `events.json`
2. Consumer accepts/rejects the event
3. Consumer saves to file or sqlite db