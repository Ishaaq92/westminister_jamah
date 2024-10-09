from flask import Flask, render_template
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests

url = "https://mayfairislamiccentre.org.uk/prayer-time/"
app = Flask(__name__)

def get_today_jamaa_times(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html')
	table = soup.find_all('table')[0]
	today_day = datetime.now().day
	columns_to_keep = [0, 2, 5, 7, 9, 11]
	today_jamaa_times = None

	for row in table.find_all('tr')[4:]:
		cells = row.find_all('td')
		day_of_month = int(cells[0].text.strip())
		if day_of_month == today_day:
			today_jamaa_times = [cells[i].text.strip() for i in columns_to_keep]
			break
	return today_jamaa_times

@app.route('/')
def show_prayer_times():
	# Retrieve today's Jamaa times
	jamaa_times = get_today_jamaa_times(url)

	# Pass the prayer times to the template
	return render_template('prayer_times.html', jamaa_times=jamaa_times)

if (__name__ == '__main__'):
	app.run()
