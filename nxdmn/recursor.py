"""
Write code for your recursor here.

You may import library modules allowed by the specs, as well as your own other modules.
"""

import pathlib
from sys import argv
import socket
import time
import typing

def domain_resolver(domain, server, timeout):
    '''
    Domain resolver function. 
    Resolves domain using TLD, authoritative nameservers. 
    '''

    # Split domain, send last part (A in C.B.A format) to root server.
    domain_parts = domain.split('.')
    a = domain_parts[-1]

    server.sendall((a + '\n').encode())
    server.settimeout(timeout) 

    # Recieve TLD port
    tld_port = server.recv(1024).decode('utf-8').strip()

    # If server response is NXDOMAIN print NXDOMAIN
    if tld_port == "NXDOMAIN":
        print("NXDOMAIN", flush = True)
        exit()
    
    # Connect to TLD nameserver
    try: 
        tld_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tld_server.settimeout(timeout) 
        tld_server.connect(("", int(tld_port)))

        # Send last and second last parts of domain (B.A in C.B.A format) to TLD server
        b_a = domain_parts[-2] + "." + a
        tld_server.sendall((b_a + '\n').encode())

        # Recieve authoritative port
        auth_port = tld_server.recv(1024).decode('utf-8').strip()
        tld_server.close()

        if auth_port == "NXDOMAIN":
            print("NXDOMAIN", flush = True)
            exit()
    
    # Print error message if connection unsuccesful
    except ConnectionRefusedError:
            print("FAILED TO CONNECT TO TLD", flush = True)
            exit()

    # Print NXDOMAIN if timeout reached
    except TimeoutError:
        print("NXDOMAIN")

    # Connect to authoritative nameserver
    try:
        auth_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auth_server.settimeout(timeout) 
        auth_server.connect(("", int(auth_port)))

        # Send entire domain (C.B.A in C.B.A format) to authoritative nameserver
        auth_server.sendall((domain + '\n').encode())

        # Recieve port of queried domain
        final_port = auth_server.recv(1024).decode('utf-8').strip()
        auth_server.close()

        # Print port of queried domain
        print(final_port, flush = True)

    except ConnectionRefusedError:
            print("FAILED TO CONNECT TO AUTH", flush = True)
            exit()

    except TimeoutError:
        print("NXDOMAIN")

def init():
    '''
    Initializer function. 
    Connects to root nameserver. 
    Returns root nameserver, timeout.
    '''

    try:
        root_port = int(argv[1])

        # Validate root port
        if root_port < 1024 or root_port > 65535:
            print("INVALID ARGUMENTS", flush = True)
            exit() 
        
        timeout = float(argv[2])

        if (len(argv) > 3):
            print("INVALID ARGUMENTS", flush = True)
            exit()
        
        # Validate timeout
        if not isinstance(timeout, (int, float)):
            print("INVALID TIMEOUT\n", flush = True)

        try:
            # Connect to root nameserver
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(timeout) 
            server.connect(("", root_port))
        
            return server, timeout

        # Check if port in appropriate range
        except OverflowError:
            print("INVALID ARGUMENTS", flush = True)
            exit()
        
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO ROOT", flush = True)
            exit()
        
        except TimeoutError:
            print("NXDOMAIN")

    except IndexError:
        print("INVALID ARGUMENTS", flush = True)
        exit()

def valid_domain(domain):
    '''
    Domain validating function. 
    Validates domains. 
    Returns boolean validity of domain.
    '''
    
    def valid_part(segment):
        '''
        Valid part helper function. 
        Validates section (B or A in C.B.A format) of domain. 
        '''

        # check if section is alphanumeric or contains hyphen  "-"
        return all(char.isalnum() or char == '-' for char in segment) 

    def valid_c(segment):
        '''
        Valid 'C' helper function. 
        Validates last section (C in C.B.A format) of domain. 
        '''

        # Split parts via ".", validate each part.
        return all(valid_part(part) for part in segment.split('.')) and not segment.startswith('.') and not segment.endswith('.')

    # Split domain into segments, validate.
    segments = domain.split('.')

    if len(segments) == 3: 
        c, b, a = segments
        if valid_c(c) and valid_part(b) and valid_part(a):
            return True

    # Partial domain validation.
    elif len(segments) in [1, 2]:  
        if len(segments) == 1:
            return valid_part(segments[0]) 
        else:
            b, a = segments
            if valid_part(b) and valid_part(a):
                return True
    
    # Validate segments in longer C.B.A format. E.g: alice.bob.carol.dan.eve.
    elif len(segments) > 3:
        a, b = segments[-1], segments[-2]  
        if not (valid_part(a) and valid_part(b)):
            return False
        
        # Validate each segment inside the 'C' part
        for seg in segments[:-2]:  
            if not valid_part(seg):
                return False
        return True

    return False

def main(args: list[str]) -> None:
    '''
    Main function. 
    Run init, domain resolver functions
    '''

    server, timeout = init()

    # Continuously resolve domains from user input
    while True:
        try:

            domain = input("")  
            if not domain:
                break

            if not valid_domain(domain):
                print("INVALID", flush = True)
                continue

            domain_resolver(domain, server, timeout)

        except EOFError:
            break


    pass 

if __name__ == "__main__":
    main(argv[1:])





