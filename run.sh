#!/bin/sh

set -e

exec pipenv run python3 -m demo.main "$@"
