#!/bin/bash

python3 upload_weed25.py --label crabgrass &
python3 upload_weed25.py --label goosefoots &
python3 upload_weed25.py --label green_foxtail &
python3 upload_weed25.py --label purslane &
wait