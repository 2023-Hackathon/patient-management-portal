#!/bin/sh

pip install -r requirements.txt

streamlit run your_script.py --server.port 80
