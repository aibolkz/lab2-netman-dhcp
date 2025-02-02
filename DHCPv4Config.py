#/usr/bin/env python3
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

#r1, r2, r3 routers 
devices = {
    "R2": {"device_type": "cisco_ios", "host": "198.51.100.1", "username": "admin", "password": "admin"},
    "R3": {"device_type": "cisco_ios", "host": "198.51.100.20", "username": "admin", "password": "admin"},
    "R4": {"device_type": "cisco_ios", "host": "198.51.100.3", "username": "admin", "password": "admin"},
}

commands = [
    'interface FastEthernet1/0',
    'ip address dhcp',
    'no shut',
    ]


def configure_router(router_name, details):
    """connection to the routers """
    print(f"Connection to {router_name} ({details['host']})...")

    try:
        # connection to Routers
        net_connect = ConnectHandler(**details)
        print(f"COnnected to {router_name}")

        output = net_connect.send_config_set(commands)
        print(output)
        
        net_connect.save_config()
        net_connect.disconnect()

    except Exception as e:
         print(f"Couldnt connect to {router_name}: {e}")
    

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(configure_router, name, details): name for name, details in devices.items()}

print(" all routers are configured")
