#!/usr/bin/env python3

import os
import sys
import requests
from jinja2 import Environment, Template

# Constants
DEFAULT_LIMIT = 1000

# SSH config template
SSH_CONFIG_TEMPLATE = """# Devices

{%- for device in netbox_devices.results %}
{%- if device.primary_ip and device.primary_ip.address %}

# Netbox URL: {{ device.url }}
Host {{ device.name}}
    User {{ ssh_user }}
    Hostname {{ device.primary_ip.address.split("/")[0] }}
    Port {{ ssh_port }}
    IdentityFile {{ ssh_key }}

{%- endif %}
{%- endfor %}

# Virtual Machines
{%- for vm in netbox_vms.results %}
{%- if vm.primary_ip and vm.primary_ip.address %}

# Netbox URL: {{ vm.url }}
Host {{ vm.name}}
    User {{ ssh_user }}
    Hostname {{ vm.primary_ip.address.split("/")[0] }}
    Port {{ ssh_port }}
    IdentityFile {{ ssh_key }}

{%- endif %}
{%- endfor %}
"""

def get_env_var(name, required=True, default=None):
    """Get environment variable with optional default."""
    value = os.getenv(name, default)
    if required and not value:
        print(f"Error: Environment variable {name} is required but not set")
        sys.exit(1)
    return value

def fetch_netbox_data(url, token, endpoint):
    """Fetch data from NetBox API endpoint."""
    headers = {
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
    }
    
    try:
        response = requests.get(f"{url}/api/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        sys.exit(1)

def main():
    # Get environment variables
    netbox_url = get_env_var('NETBOX_URL')
    netbox_token = get_env_var('NETBOX_TOKEN')
    ssh_user = get_env_var('SSH_USER')
    ssh_port = get_env_var('SSH_PORT', required=False, default='22')
    ssh_key = get_env_var('SSH_PRIVATE_KEY_PATH', default='~/.ssh/id_rsa')
    ssh_config_path = get_env_var('SSH_CONFIG_PATH', required=False, default='~/.ssh/config')
    
    # Remove trailing slash from URL if present
    netbox_url = netbox_url.rstrip('/')
    
    # Fetch data from NetBox
    print("Fetching devices from NetBox...")
    netbox_devices = fetch_netbox_data(netbox_url, netbox_token, f'dcim/devices/?primary_ip4__empty=False&limit={DEFAULT_LIMIT}')
    
    print("Fetching virtual machines from NetBox...")
    netbox_vms = fetch_netbox_data(netbox_url, netbox_token, f'virtualization/virtual-machines/?primary_ip4__empty=False&limit={DEFAULT_LIMIT}')
    
    print(f"Found {len(netbox_devices['results'])} devices and {len(netbox_vms['results'])} VMs")
    
    # Load and render template
    template = Template(SSH_CONFIG_TEMPLATE)
    
    # Render SSH config
    ssh_config = template.render(
        netbox_devices=netbox_devices,
        netbox_vms=netbox_vms,
        ssh_user=ssh_user,
        ssh_port=ssh_port,
        ssh_key=ssh_key
    )
    
    # Expand tilde in path
    ssh_config_path = os.path.expanduser(ssh_config_path)
    
    # Save SSH config to file
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(ssh_config_path), exist_ok=True)
        
        with open(ssh_config_path, 'w') as f:
            f.write(ssh_config)
        
        print(f"SSH config saved to: {ssh_config_path}")
        
    except Exception as e:
        print(f"Error writing SSH config to {ssh_config_path}: {e}")
        print("\n# Generated SSH Config")
        print(ssh_config)

if __name__ == '__main__':
    main()