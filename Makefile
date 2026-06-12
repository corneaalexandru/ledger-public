.PHONY: run setup check

run:
	python3 server.py --store google --open

setup:
	python3 scripts/setup_google.py

check:
	python3 -m py_compile server.py
	python3 scripts/check_public_release.py
