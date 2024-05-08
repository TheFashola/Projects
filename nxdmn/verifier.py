"""
Write code for your launcher here. hi

You may import library modules allowed by the specs, as well as your own other modules.
"""

import pathlib
from sys import argv
import socket
import time
import typing


def main(args: list[str]) -> None:
    '''
    Main function. 
    Validates master and single files. 
    '''

    if len(argv) != 3:
        print("invalid arguments")
        exit()

    try:

        # Validate master file 
        master_file = pathlib.Path(argv[1])

        if not master_file.exists() or not master_file.is_file():
            raise FileNotFoundError

        with master_file.open('r') as file:
            root_port = int(file.readline())
            
            # Validate root port in master file
            if root_port < 1024 or root_port > 65535:
                print("invalid master")
                exit() 
            
        with master_file.open('r') as file:

            try:

                # Validate individual domain ports in master file
                line = file.readline()
                domain_port = line.split(",")

                if int(domain_port[1])  < 1024 or int(domain_port[1]) > 65535:
                    print("invalid master")
                    exit() 

            except IndexError:
                print("invalid master")


        directory_of_single_files = pathlib.Path(argv[2])

        for file in [f for f in directory_of_single_files.iterdir() if f.is_file()]:
            
            with file.open() as f:
                    
                    # Validate root port in each single file
                    root_port = int(f.readline().strip())

                    if root_port < 1024 or root_port > 65535:
                        print("invalid single")
                        exit()
                    
                    # Validate individual domain ports in each single file
                    line = f.readline().strip()
                    _, port = line.split(',')

                    port = int(port)
                    if port < 1024 or port > 65535:
                        print("invalid single")
                        exit() 

        # Validate directory 
        if not directory_of_single_files.exists() or not directory_of_single_files.is_dir():
            print("SINGLES IO ERROR")
            exit()

    except FileNotFoundError:
        print("invalid master")
        exit()

    except ValueError:
        print("invalid master")
    


if __name__ == "__main__":
    main(argv[1:])
