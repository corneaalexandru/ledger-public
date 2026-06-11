.PHONY: run setup starter check

run:
	python3 server.py --store google --open

setup:
	python3 scripts/setup_google.py

starter:
	python3 server.py --create-starter-workbook

check:
	python3 -m py_compile server.py
	python3 scripts/check_public_release.py
