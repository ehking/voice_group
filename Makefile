dev:
bash run_dev.sh

fmt:
black backend models worker tests

lint:
flake8 backend models worker

.PHONY: dev fmt lint
