#!/bin/bash
exec gunicorn -b 0.0.0.0:8080 flaskServer:app --workers 4

