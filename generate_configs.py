"""
Script to create files for sending devices configurations to NSO local install
"""

import json
import os
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = "configs"

# Load template from a file
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("device_config_template.j2")

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Load list of devices from JSON file
with open("devices.json", "r", encoding="utf-8") as file:
    devices = json.load(file)


# Mapping OS to NED ID
ned_id_map = {
    "ASA": "cisco-asa-cli-6.18",
    "IOS": "cisco-ios-cli-6.91",
    "IOS-XR": "cisco-iosxr-cli-7.45",
    "NX-OS": "isco-nx-cli-5.23",
}


# Filter non-configurable devices
configurable_devices = [d for d in devices if d["os"] != "Linux"]


for device in configurable_devices:
    config = template.render(
        name=device["name"],
        address=device["address"],
        authgroup="labadmin",
        ned_id=ned_id_map[device["os"]],
        protocol="telnet",
        ned_settings=device.get("ned_settings", False),
    )

    # Save configuration to a file
    file_name = device["name"]
    FILE_EXT = "txt"
    file_path = os.path.join(OUTPUT_DIR, f"{file_name}.{FILE_EXT}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(config)
    print(f"Device configuration saved in: {file_name}")
