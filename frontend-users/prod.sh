#!/bin/sh

pip install -r requirements.txt

streamlit run index.py --server.port 8080
