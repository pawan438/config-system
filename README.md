# config-system
# Config-Driven System

Reads a JSON config file and simulates system behavior based on it.

## Project Structure

```
config-system/
├── config/
│   └── config.json      # all settings live here
├── logs/
│   └── system.log       # auto-created on first run
├── main.py              # main logic
└── README.md
```

## How to Run

```bash
python3 main.py
```

## Config Fields

| Field                      | Type    | Values          |
|----------------------------|---------|-----------------|
| service_name               | string  | any name        |
| environment                | string  | "dev" or "prod" |
| features.logging_enabled   | bool    | true / false    |
| features.metrics_enabled   | bool    | true / false    |
| features.maintenance_mode  | bool    | true / false    |

## What It Does

- Reads `config/config.json`
- Validates all required fields exist
- Prints behavior based on environment and feature flags
- Logs everything to `logs/system.log`
- Exits with code `1` on any critical error
