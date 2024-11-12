#!/bin/bash

# 1. Arg: Entferne alte Daten
# 2. Arg: Lade Rohdaten herunter
# 3. Arg: Daten vorverarbeiten
# 4. Arg: Optionale Argumente (test), wordurch ein Teil der SQL ausgegeben wird
python3 datapipline.py clean download prepare "$@"