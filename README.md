# Netbox to SSH Config

A simple script to convert Netbox device and virtual machine data to an SSH config file. Very useful if you're using another tool that uses existing SSH config like VSCode or [lazyssh](https://github.com/Adembc/lazyssh) and already have a Netbox instance set up.

## Assumptions

Since I currently only uses this script for myself, currently the script only supports some bare minimum for my needs:
- It only tracks devices and virtual machines with a primary IP;
- It uses the same username and SSH key that are defined using environment variables for all connections, so it only supports one username and SSH key;
- I set a hardcoded limit of 1000 entries for each device and VMs.

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
