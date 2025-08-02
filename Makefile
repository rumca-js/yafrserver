#
# Assuming: you have python poetry installed
# sudo apt install python3-poetry
#
# if poetry install takes too long
# export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
#
# yt-dlp needs to be callable from path https://github.com/yt-dlp/yt-dlp/wiki/Installation
#
.PHONY: install installsysdeps
.PHONY: run
.PHONY: reformat
.PHONY: backfiles test

CP = cp
PROJECT_NAME = crawler-buddy

# Assumptions:
#  - python poetry is in your path

install:
	poetry install

server:
	poetry run python yafrserver.py

# Assumptions:
#  - python black is in your path
# Black should use gitignore files to ignore refactoring
reformat:
	poetry run black rsshistory
	poetry run black utils
	poetry run black *.py

backfiles:
	find . -type f -name "*.bak" -exec rm -f {} +

test:
	poetry run python -m unittest discover -v
