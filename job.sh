#!/bin/bash

# EDIT THE <INSTALL PATH>
source <INSTALL PATH>/venv/bin/activate
cd <INSTALL PATH>/

# EDIT <REGISTRAR> <DOMAIN>
python ddnshelper.py <REGISTRAR> <DOMAIN>

deactivate
