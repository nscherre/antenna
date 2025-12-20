#!/bin/bash
set -euo pipefail
find . -name '__pycache__' -o -name '*.egg-info' | xargs rm -rf
