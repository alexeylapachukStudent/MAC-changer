#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def return_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # change ifconfig_result to str(ifconfig_result)to be able launch this code for Python 3
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


def check_entered_mac_address(current_mac_address, options_mac):
    if current_mac_address == options_mac:
        print("[+] MAC address was successfully changed to " + current_mac_address)
    else:
        print("[-] MAC address was not changed")


options = get_arguments()
current_mac = return_mac_address(options.interface)
print("Current MAC address = " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = return_mac_address(options.interface)
check_entered_mac_address(current_mac, options.new_mac)
