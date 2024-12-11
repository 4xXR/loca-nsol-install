# NSO Configuration Automation

This project automates the generation and deployment of configurations for network devices using Cisco NSO (Network Services Orchestrator). The configurations are dynamically created using Jinja2 templates and can be deployed via RESTCONF or CLI.

## Features
- **Dynamic Configuration Generation**: Uses Jinja2 templates to create configurations for various device types.
- **Device-Specific Logic**: Supports additional settings (e.g., `ned-settings`) for specific devices.
- **CLI Deployment**: Automates the deployment of configurations via the NSO CLI.

## Prerequisites
- Python 3.7+
- Cisco NSO installed on the Devbox (sandbox environment). The "local-NSO-install" on the Linux DevBox was used.
- A project directory structure with:
  - `device_config_template.j2` (Jinja2 template)
  - `devices.json` (Device configuration list)
  - Python scripts for configuration generation and deployment.

## Setup Instructions

### Step 1: Generate Configurations
Use the Python script to generate configurations dynamically for devices listed in `devices.json`.

```python
from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("device_config_template.j2")

# Load devices from JSON file
with open("devices.json", "r") as file:
    devices = json.load(file)

# Generate configurations and save to files
for device in devices:
    config = template.render(
        name=device["name"],
        address=device["address"],
        authgroup="labadmin",
        ned_id=device["ned_id"],
        protocol="telnet",
        ned_settings=device.get("ned_settings", False)
    )
    filename = f"{device['name']}_config.txt"
    with open(filename, "w") as f:
        f.write(config)
    print(f"Configuration saved to {filename}")
```
### Step 2: Deploy Configurations via CLI
- Copy the generated configuration files to the Devbox using scp.
- Run the bash script on the Devbox to load configurations into NSO.
- Verify the configurations in NSO:
-     ncs_cli -u admin
-     show running-config devices


