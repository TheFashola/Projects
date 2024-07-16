"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""

# TO RUN: python3 server.py tests/sample.conf  

import pathlib
from sys import argv
import socket
import time
import typing


def init():
    '''
    Initializer function. 
    Parses config file into dictionary.
    Returns root port, config dictionary
    '''

    try:
        if len(argv) != 2:   
            print("INVALID ARGUMENTS")
            exit()

        path = argv[1]
        filepath = pathlib.Path(path)

        with filepath.open('r') as file:
            root_port = file.readline()
            config = {}

            # Populate config dictionary with [domain, port] using .split(",").
            for lines in file:
                parts = lines.strip().split(",")

                config_domain = parts[0] 
                config_port = parts[1] 
                config[config_domain.strip()] = config_port.strip()

                if int(parts[1]) < 1024 or int(parts[1]) > 65535:
                    print('INVALID CONFIGURATION')
                    exit()

    # Error handling: config file invalid if FileNotFoundError raised.
    except FileNotFoundError:
        print('INVALID CONFIGURATION')
        exit()

    except IndexError:
        print("INVALID ARGUMENTS")
        exit()
    
    return root_port, config


def server(root_port, config):
    '''
    Server function. 
    Continuously sends port(s) of queried domain(s) to recursor. 
    Also handles commands, logging to stdout.
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(("", int(root_port)))
        s.listen(5) 

    # If root port is invalid, socket error raised.
    except socket.error: 
        print('INVALID CONFIGURATION')
        exit()

    # Continuously send port of queried domain to recursor
    while True:
            recursor, _ = s.accept()
            data = recursor.recv(1024).decode('utf-8').strip()

            # Check if data from recursor is a command
            if "!" not in data:
                    port = config.get(data)

                    # If queried domain has no port, send NXDOMAIN to recursor and log to stdout.
                    if port is None:
                        recursor.send("NXDOMAIN\n".encode('utf-8'))
                        print(f"resolve {data} to NXDOMAIN", flush = True)

                    # Else, send queried port to recursor and log to stdout.
                    else:
                        recursor.send((port + "\n").encode('utf-8'))
                        print(f"resolve {data} to {port}", flush = True)

            # Close server if exit command recieved
            elif data == "!EXIT\n":
                s.close()
                exit()

            # Add [domain, port] to config dictionary 
            elif  "!ADD" in data:
                data_parts = data.split()
                domain, port = data_parts[1], data_parts[2]
                config[domain] = port

            # Remove [domain, port] from config dictionary 
            elif  "!DEL" in data:
                data_parts = data.split()
                domain = data_parts[1]
                config.pop(domain)

def main(args: list[str]) -> None:
    '''
    Main function. 
    Run init, server functions
    '''

    root_port, config = init()
    server(root_port, config)


if __name__ == "__main__":
    main(argv[1:])