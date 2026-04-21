import yaml
import pandas as pd


def load_config(path):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            if config is None:
                raise ValueError("Config file is empty")
    except FileNotFoundError:
        raise ValueError("Config file not found")
    except yaml.YAMLError:
        raise ValueError("Invalid YAML format")

    for key in ["seed", "window", "version"]:
        if key not in config:
            raise ValueError(f"Missing config field: {key}")

    return config


def load_data(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise ValueError("Input CSV file not found")

    if not lines:
        raise ValueError("Input CSV is empty")

    rows = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        row = [v.strip() for v in line.split(",")]
        rows.append(row)

    if not rows:
        raise ValueError("Input CSV is empty")

    df = pd.DataFrame(rows[1:], columns=rows[0])

    df.columns = [c.lower().strip() for c in df.columns]

    if "close" not in df.columns:
        raise ValueError(
            f"Missing required column: close. Columns found: {df.columns.tolist()}"
        )

    return df
