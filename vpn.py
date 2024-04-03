import platform
import random
import os
import time
import requests

# List of countries that a VPN can be randomly selected from

countries = ['United States', 'Canada', 'Mexico', 'United Kingdom', 'Germany',
             'France', 'Netherlands', 'Sweden', 'Switzerland', 'Denmark', 'Poland', 'Italy', 'Spain', 'Norway',
             'Belgium', 'Ireland', 'Finland', 'Japan', 'Hong Kong', 'New Zealand', 'South Korea']


class VPN:
    def __init__(self):

        # Set up for working with standard NordVPN installation directory

        self.path = 'C:/Program Files/NordVPN'

    # Function to randomly pick a country from the list, then connect to a VPN from that country

    def nordvpn_connect(self):
        os.chdir(self.path)
        command = 'nordvpn -c -g \'' + random.choice(countries)
        # print(os.getcwd())
        os.system(command)

        # Giving some additional time so that NordVPN has a chance to fully connect
        time.sleep(10)

    # Function to check current IP address

    def ip_check(self):
        ip = requests.get('https://api.ipify.org').text
        print(f'IP Address: {ip}')

    # Function to disconnect from current VPN connection

    def nordvpn_disconnect(self):
        os.chdir(self.path)
        os.system('nordvpn -d')
        time.sleep(3)
