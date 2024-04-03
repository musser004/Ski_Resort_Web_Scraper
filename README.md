# Project: Ski Resort Web Scraper (Automation)

Demo video: https://youtu.be/UJE38xQqJAU

Description: Web scraper designed to automatically connect to a VPN (from a randomly selected country), bypass Captcha on a ski resort website (if present), obtain API cookie, close window and disconnect from VPN, automatically reconnect to another VPN (from another randomly selected country), then use the API cookie to pull ski resort ticket price data over a customizable range of dates and age groups. Data is exported into an output CSV file.

Python Libraries: Selenium, Json, Requests, OS, CSV, Datetime, Capsolver, Urllib

NOTE: Application requires environmental variables (not included) in order to run captcha_solver.py properly

# How to use:

- Update "WORKING_PATH" and "GLOBAL_PATH" in Whistler.py and captcha_solver.py
- Add CapSolver API Key as "API_KEY" environmental variable to properly run captcha_solver.py
- Install packages from requirements.txt
- Install NordVPN in standard directory, or update the installation directory path in vpn.py
- Run Whistler.py
