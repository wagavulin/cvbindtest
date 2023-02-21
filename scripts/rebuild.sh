#!/bin/bash

set -ex
./scripts/cleanup.sh
./gen2rb.py
ruby extconf.rb
make
