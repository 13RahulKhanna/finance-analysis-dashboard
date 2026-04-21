# MLOps Batch Job – Trading Signal Pipeline

## Overview
This project implements a minimal MLOps-style batch job that:
- Loads config from YAML
- Processes OHLCV market data
- Computes rolling mean and binary trading signal
- Outputs structured metrics and logs
- Runs locally and inside Docker

## Requirements
- Python 3.9+
- Docker (optional)

## Local Run

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log