import subprocess


def select_network_adapter():
    try:
        subprocess.run(["netsh", "interface", "ipv4", "show", "interfaces"], check=True)
        interface_number = input(
            "Enter the interface number of the network adapter to use: "
        )
        return interface_number
    except subprocess.CalledProcessError as e:
        print(f"Error selecting network adapter: {e.stderr.decode().strip()}")
        return None


def add_route(destination_ip, network_adapter_ip, interface_number):
    try:
        subprocess.run(
            [
                "route",
                "add",
                destination_ip,
                "mask",
                "255.255.255.255",
                network_adapter_ip,
                "metric",
                "10",
                "if",
                interface_number,
            ],
            check=True,
        )
        print("Route added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding route: {e.stderr.decode().strip()}")


# Sample destination IP
destination_ip = "192.168.1.100"

# Select the network adapter
interface_number = select_network_adapter()
if interface_number is not None:
    # Get the IP address of the selected network adapter
    network_adapter_ip = (
        subprocess.check_output(
            [
                "netsh",
                "interface",
                "ipv4",
                "show",
                "config",
                f"interface={interface_number}",
            ]
        )
        .decode()
        .split("\n")[35]
        .split(":")[1]
        .strip()
    )

    # Add the route
    add_route(destination_ip, network_adapter_ip, interface_number)
