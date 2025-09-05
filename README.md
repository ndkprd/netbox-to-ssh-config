# Netbox to SSH Config

A simple script to convert Netbox device and virtual machine data to an SSH config file.

## Assumption

Since I basically only use this script for myself, currently the script only supports the following assumptions:
- Use the same username for all SSH connections;
- Use the same port for all SSH connections, defaults to 22;
- Use the same SSH key for all SSH connections.

## Usage

Set the following environment variables:
- `NETBOX_URL`: The URL to your Netbox instance, e.g. `https://netbox.example.com`;
- `NETBOX_TOKEN`: The API token for your Netbox instance. For permissions, read permission for Virtual Machine and Device resources should be more than enough;
- `SSH_USER`: The username to use for SSH connections;
- `SSH_PORT`: The port to use for SSH connections, defaults to 22;
- `SSH_PRIVATE_KEY_PATH`: The path to the SSH key to use for SSH connections;
- `SSH_CONFIG_PATH`: The path to save the generated SSH config file, defaults to `~/.ssh/config`.

Install the requirements:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python netbox_to_ssh.py
```

## License

[MIT](./LICENSE)
