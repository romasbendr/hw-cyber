.PHONY: install run-propagator run-consumer run-tests

install:
	poetry install

run-propagator:
	poetry run python propagator/event_propagator.py

run-consumer:
	poetry run uvicorn consumer.event_consumer:app \
	--port $$(poetry run python -c "from consumer.configuration.config import settings; print(settings.CONSUMER_PORT)")

run-tests:
	poetry run pytest -v