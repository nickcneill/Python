'''
Author: Nicholas Neill
Date: 11/16/2017
Interpreter: 3.6.3
IDE: PyCharm
Description: Lite TCP port scanner for penetration testing and network security.
Version: PSCAN 0.9.1
'''

import socket
import time
from datetime import datetime
import os


# function for clearing console window:
# takes two arguments, Wait time in seconds and a 1 to exit or a 0 to continue
def clear(wait=0, close=0):
    # optional parameter to allow a message some time to be read before clearing console.
    time.sleep(wait)
    # statement to issue os command to proper OS
    if close == 0:  # Used in exceptions, Continues from the  EX point.
        if os.name == "nt":  # Handle Windows NT consoles
            os.system("cls")
        else:  # should work for all other OS's
            os.system("clear")
    elif close == 1:  # restarts the application.
        if os.name == "nt":  # Handle Windows NT consoles
            os.system("cls")
        else:  # should work for all other OS's
            os.system("clear")
        user_input()
    elif close == 2:  # quits the application.
        quit()


def user_input():  # Handle input and process it
    input_tries = 4  # limits the number of attempts to correctly input a value
    for tries in range(input_tries):
        input_tries -= 1
        try:  # hopefully get usable input:
            remote_server = input("Enter a remote host to scan: ")
            # Handle erroneous inputs:
            if remote_server == "":
                raise ValueError("No input detected!")  # Retries if there is no input
            else:  # Input es bueno
                remote_server_ip = socket.gethostbyname(remote_server)  # Resolves host name to IPv4 address
                break  # Breaks try-loop because input was good
        except ValueError as e:  # Here is where the exception is dealt with
            if input_tries is not 0:  # If there are tries left...
                print(e, "\n", input_tries, "Tries left")
                clear(2)
            else:  # Out of tries
                print("No Input was received now quiting")
                clear(2, 1)
        except socket.gaierror:  # If we fail at resolving hostname to IPv4 Address
            if input_tries is not 0:  # If there are tries left...
                print(remote_server, ' could not be resolved. Please try again')
                clear(2)
            else:  # Out of tries
                print("No Input was received now quiting")
                clear(2, 2)  # Failure threshold reached and application quits
    input_tries = 4

    # now we handle the input for our port range same for loop for Remote Server IP
    for tries in range(input_tries):
        input_tries -= 1
        try:
            port_range = input('Input port range to scan: ')
            ports = [int(i) for i in port_range.split() if i.isdigit()]  # Filter input in to digits only
            if port_range == "":  # Handle no input
                raise ValueError("No input detected! Tries left: ")
            elif not ports:  # Handle input that when filtered using the isdigit() func results in Null
                raise ValueError("Could not handle your input try entering port(s) in another way")
            elif len(ports) <= 2:  # If true then we either have single Port or Range of Ports to scan
                start_port = min(ports)  # Using the range function we can handle both ranges
                end_port = max(ports)  # or single ports
                range_scan(start_port, end_port, remote_server_ip)  # pass arguments to range_scan function.
                break  # Input is good ---> break try loop
            elif len(ports) > 2:  # List of port numbers to scan.
                targeted_scan(ports, remote_server_ip)  # pass arguments to targeted_scan function
        except ValueError as e:  # Excepts invalid input
            if input_tries is not 0:  # Checks if user has tries left
                print(e, input_tries)  # prompts user to try again and displays number of tries left
                clear(2)
            else:  # No tries left and exits the application
                print("No valid input was received now quiting")
                clear(2, 2)


def range_scan(start, end, ip):
    print("*" * 27, 'PSCAN', "*" * 26)  # creates banner same as batch file
    if start == end:  # isolates single port use cases
        print("Starting scan of port: ", end, "on ", "(", ip, ")")
    else:  # uses input from user_input function as range of ports
        print("Starting scan of port:", start, "to", end, "on ", "(", ip, ")")
    print("*" * 60)
    start_time = datetime.now()  # Get start time
    try:  # Keep scan alive if a port returns unexpected value
        for port in range(start, end + 1):  # + to include final port #
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # use socket module to create object
            result_tcp = sock_tcp.connect_ex((ip, port))  # Connect_EX function returns '0' when TCP Conn Accepted
            if result_tcp == 0:  # Connection accepted
                result = "Port {}:          Open TCP".format(port)  # Format everything nice and slick
            else:  # Connection refused
                result = "Port {}:          Closed".format(port)
            print(result)
            sock_tcp.close()  # end port scan

    except socket.error:
        print("Connection Refused")
        clear(2, 1)

    except KeyboardInterrupt:
        print("Canceled By User")
        clear(2, 1)
    finish(start_time)  # Pass the port scan start time as argument to finsh fucntion


def targeted_scan(targets, ip):
    print("*" * 27, 'PSCAN', "*" * 26)
    print("Starting TARGETED scan of port: ", targets, "on ", "(", ip, ")")
    print("*" * 60)

    # check scan_time
    start_time = datetime.now()

    try:
        for port in targets:  # targets is a list that can easily be enumerated.
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result_tcp = sock_tcp.connect_ex((ip, port))
            if result_tcp == 0:  # Connection accepted
                result = "Port {}:          Open TCP".format(port)  # Format everything nice and slick
            else:  # Connection refused
                result = "Port {}:          Closed".format(port)
            print(result)
            sock_tcp.close()

    except socket.error:
        print("Connection Refused")
        clear(2, 1)
    except KeyboardInterrupt:
        print("Canceled By User")
        clear(2, 1)
    finish(start_time)  # Pass the port scan start time as argument to finsh fucntion


# option to make ports into objects but UDP results wont work with Connect_EX
# because UDP is connectionless Socket assumes it is sent and does not handle closed ports.

''' 

class PortStatus(object):
    def __init__(self, tcp, udp, number):
        self.tcp = tcp
        self.udp = udp
        self.number = number
        return PortStatus.status()

    def status(self):
        tcp = PortStatus.tcp
        udp = PortStatus.udp
        number = PortStatus.number
        if tcp and udp == 0:
            result = "Port {}:      Open TCP/UDP".format(number)
        elif tcp == 0 and udp != 0:
            result = "Port {}:      Open TCP".format(number)
        elif udp == 0 and tcp != 0:
            result = "Port {}:      Open UDP".format(number)
        else:
            result = "Port {}:      Closed".format(number)
        return result


'''


def finish(start_time):
    # Check end_time
    end_time = datetime.now()

    # prints total elapsed time:
    print("Finished scan in: ", end_time - start_time)
    rescan = input("Scan Again Y/N? :")
    if rescan == 'y':
        print("Starting new scan!")
        clear(1)
        user_input()
    else:
        print("PSCAN is Exiting")
        clear(1, 2)


def main():
    user_input()


main()
