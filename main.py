#!/usr/bin/env python3
# Config-Driven System
# Reads a JSON config file and simulates system behavior based on it

import json
import os
from datetime import datetime

# path to config and log files
CONFIG_FILE = "config/config.json"
LOG_FILE    = "logs/system.log"

# -------------------------------------------------------
# function to log messages with timestamp to file + screen
# -------------------------------------------------------
def log_message(message):
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')
    log_line  = f"[{timestamp}] {message}"

    print(log_line)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)  # create logs/ if missing
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

# -------------------------------------------------------
# function to read config.json and return it as a dict
# -------------------------------------------------------
def read_config():
    if not os.path.exists(CONFIG_FILE):         # check file exists before opening
        log_message("ERROR: config.json not found")
        exit(1)

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)                   # parse JSON into python dict

    return config

# -------------------------------------------------------
# function to validate required fields in config
# -------------------------------------------------------
def validate_config(config):
    required_fields = ["service_name", "environment", "features"]

    for field in required_fields:               # loop through each required field
        if field not in config:
            log_message(f"CRITICAL: Missing field -> '{field}'")
            return False                        # stop and return False if any missing

    env = config["environment"]
    if env not in ["dev", "prod"]:              # environment must be dev or prod only
        log_message(f"CRITICAL: environment='{env}' is invalid. Use 'dev' or 'prod'")
        return False

    return True                                 # all checks passed

# -------------------------------------------------------
# function to simulate system behavior based on config
# -------------------------------------------------------
def apply_config(config):
    service  = config.get("service_name", "unknown")   # .get() avoids KeyError if missing
    env      = config.get("environment")
    features = config.get("features", {})              # default to empty dict if missing

    log_message(f"Starting service  : {service}")
    log_message(f"Environment       : {env}")

    # dev vs prod behaviour check
    if env == "dev":
        log_message("MODE: Debug logging ON — verbose output enabled")
    elif env == "prod":
        log_message("MODE: Production — minimal logging, high performance")

    # check each feature flag and print what is ON or OFF
    if features.get("logging_enabled"):
        log_message("FEATURE: Logging        -> ON")
    else:
        log_message("FEATURE: Logging        -> OFF")

    if features.get("metrics_enabled"):
        log_message("FEATURE: Metrics        -> ON")
    else:
        log_message("FEATURE: Metrics        -> OFF")

    if features.get("maintenance_mode"):        # if maintenance mode is true, stop here
        log_message("WARNING: Maintenance mode is ACTIVE — halting startup")
        exit(0)

# -------------------------------------------------------
# main execution starts here
# -------------------------------------------------------
config = read_config()
print(f"Config loaded from: {CONFIG_FILE}")
print("-" * 40)

if not validate_config(config):                 # validate before doing anything
    log_message("CRITICAL: Invalid config — exiting")
    exit(1)

apply_config(config)                            # apply logic based on config values

log_message("STATUS: All checks passed — system running normally")
exit(0)
