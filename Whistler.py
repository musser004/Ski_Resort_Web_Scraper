import json
import requests
import csv
import os.path
from datetime import datetime, timedelta, date
from vpn import VPN
from captcha_solver import CaptchaSolver

CSV_HEADERS = [
    'resort_id',
    'resort',
    'age_group',
    'product',
    'days',
    'product_date',
    'day_of_week',
    'online_price',
    'pull_date',
    'ap',
    'pct_of_adult_rate',
    'discount_advertised',
    'window_rate',
    'source'
]

WORKING_PATH = 'C:/Users/armed/Desktop/Full Stack Dev Work/Scott G/12-29-23'
GLOBAL_PATH = 'C:/Users/armed/Desktop/Full Stack Dev Work/Scott G/12-29-23/'


class ResortScraper:

    # Input data for web scraper.

    site_name = "Whistler"
    start_date = datetime.today()
    pull_date = date.today()
    age_groups = {
        "Adult": "Adult (Ages 13 - 64)",
        "Child": "Child (Ages 5 - 12)",
        "Senior": "Senior (Ages 65+)"
    }

    headers = {}

    def __init__(self):

        # Headers data is pulled in from headers.json file. This will contain the updated API key
        # (pulled by captcha_solver.py)

        os.chdir(WORKING_PATH)
        with open('headers.json') as f:
            self.headers = json.loads(f.read())
            print(self.headers)

    # Function to name/format output CSV, then append row data to it

    def write_output(self, rows):

        file_name = '{}{}-{}.csv'.format(GLOBAL_PATH,
                                         self.site_name, self.pull_date)
        is_file_existing = os.path.isfile(file_name)

        with open(file_name, 'a', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)

            if not is_file_existing:
                csv_writer.writeheader()

            for row in rows:
                csv_writer.writerow(row)

        print('{} rows are exported to {}'.format(len(rows), file_name))

    # Function to determine dates to use on API, along with requesting the data, then adding it to output CSV

    def start_exporting_resort_data(self):

        # For loop that pulls the data for every date within the given range
        # Range can be modified for days you want to fetch from, starting today (i.e. range(7), range(30), etc.)

        for dd in range(180):
            delta = timedelta(days=dd)

            rows = []
            start_date = (self.start_date+delta).strftime('%Y-%m-%d')

            # Date printed to console to show current progress of web scrape

            print(start_date)

            # Data pulled for every relevant age group (based on the age_groups input from initialization)

            for group_id in self.age_groups:
                response = requests.get(
                    url=f"https://www.whistlerblackcomb.com//api/LiftAccessApi/GetLiftTickets/{start_date}/true/{group_id}/96d317de-089d-4e27-b2ae-59bee78dc0b5",
                    headers=self.headers)

                if response.status_code != 200:
                    continue

                # Formatting JSON data

                json_data = json.loads(response.text)

                for liftTicket in json_data['LiftTickets']:
                    p_start_date = datetime.strptime(
                        liftTicket['StartDate'], "%Y-%m-%dT%H:%M:%S")
                    # p_end_date = datetime.strptime(
                    #     liftTicket['EndDate'], "%Y-%m-%dT%H:%M:%S")

                    product_date = '{}'.format(
                        p_start_date.strftime('%Y-%m-%d'))

                    # CSV row headers are defined

                    row = {
                        'resort_id':"76",
                        'resort': self.site_name,
                        'days': liftTicket['NumberOfDays'],
                        'age_group': liftTicket['AgesDisplay'],
                        # 'product_date': liftTicket['ValidForDisplay'],
                        'product_date': product_date,
                        'online_price': liftTicket['Price'],
                        'window_rate': liftTicket['WindowPrice'],
                        'ap': dd,
                        'pull_date': self.pull_date,
                        'product': liftTicket['Name']
                    }

                # Individual row is appended to overall "rows" data

                    rows.append(row)

            # Data is written to output CSV

            self.write_output(rows)


if __name__ == "__main__":

    # Opening/Connecting to a VPN in a randomly selected country

    vpn = VPN()
    vpn.nordvpn_connect()

    # Optional line below if you'd like to confirm that IP address has changed after VPN use

    # vpn.ip_check()

    # Captcha solver is brought in and solves Captcha (if necessary)

    captcha_solver = CaptchaSolver()
    captcha_solver.captcha_solve()

    # Captcha solver grabs API cookie

    captcha_solver.cookie_grab()

    # VPN is disconnected

    vpn.nordvpn_disconnect()

    # Connecting to another VPN in another randomly selected country

    vpn.nordvpn_connect()
    # vpn.ip_check()

    # Webscraper initialized with API cookie grabbed earlier, then exports data to output CSV

    scraper = ResortScraper()
    scraper.start_exporting_resort_data()

    # VPN disconnects

    vpn.nordvpn_disconnect()
