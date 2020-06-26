from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from datetime import datetime
import pandas as pd
import os

package_directory = os.path.dirname(os.path.abspath(__file__))


class HolidaysCalendar:
	def __init__(self):
		self.base_url = "http://www.seg-social.es/wps/portal/wss/internet/CalendarioLaboral"
		self.real_url = None
		self.municipalities_dropdown = "provinciasLocalidades"
		self.holiday_data_path = os.path.join(package_directory, "holiday_data/holidays.pkl")
		self.provinces = None
		self.provinces_name2id = None
		self.provinces_name2id = None

		self.current_year = datetime.now().year

		self.holidays = self.load_holidays(re_scrape=False)

	def load_holidays(self, re_scrape):
		if re_scrape or not self.cash_exists():
			# if we are manually requiring to re-scrape, be verbose
			data = self.scrape_data(verbose=re_scrape)
			self.write_cash(data)
			return data
		else:
			return self.read_cash()

	def get_holidays(self, provinces=None, municipalities=None):
		filtered_holidays = self.holidays.copy()
		# **********	province filter		**********
		# if provinces are not a list but a string, put it into a list
		if provinces:
			if not isinstance(provinces, list):
				provinces = [provinces]
			filtered_holidays = filtered_holidays[filtered_holidays["province_name"].isin(provinces)]

		# **********	municipality filter		**********
		# if municipalities are not a list but a string, put it into a list
		if municipalities:
			if not isinstance(municipalities, list):
				municipalities = [municipalities]
			filtered_holidays = filtered_holidays[filtered_holidays["local_name"].isin(municipalities)]

		return filtered_holidays

	def write_cash(self, data):
		data.to_pickle(self.holiday_data_path)

	def read_cash(self):
		try:
			return pd.read_pickle(self.holiday_data_path)
		except FileNotFoundError:
			raise Exception("Could not read holidays from cash")

	def cash_exists(self):
		return os.path.exists(self.holiday_data_path)

	def scrape_data(self, verbose=False):
		# create HTML session (with JavaScript support)
		session = HTMLSession()

		# ***************************************************************************
		# **********	  NATIONAL LEVEL: GET AVAILABLE PROVINCES		*************
		# ***************************************************************************

		soup = BeautifulSoup(session.get(self.base_url).text, 'html.parser')
		# get id of province-location dropdown form action widget in the html
		action = soup.find('form', id=self.municipalities_dropdown).get('action')
		# get all province ids available
		provinces_ids = [x["value"]for x in soup.find("select", id="Provincia").findChildren("option", recursive=False)]

		# get real URL from base object
		self.real_url = soup.find("base")["href"]

		# create empty holiday list
		holidays = []

		# ***************************************************************************
		# ********    REGIONAL LEVEL: GET AVAILABLE AUTONOMOUS REGIONS	   **********
		# ***************************************************************************
		for i, prov_id in enumerate(provinces_ids):
			# put together URL and data
			prov_data = {'Provincia': prov_id}
			post_url = "{}{}".format(self.real_url, action)
			# get data with POST method
			regional_response = BeautifulSoup(session.post(post_url, prov_data).text, 'html.parser')
			# get all location ids in the province
			municipalities_raw = regional_response.find("select", id="Localidades")
			# if there are not any municipalities, go to the next region
			if not municipalities_raw:
				continue
			# extract the municipality ids
			municipalities_ids = [x["value"] for x in municipalities_raw.findChildren("option", recursive=False)]

			# ***************************************************************************
			# ***** LOCAL LEVEL: HOLIDAYS FOR EACH (PROVINCE, REGION, MUNICIPALITY) *****
			# ***************************************************************************
			for local_id in municipalities_ids:
				# if no cod#name structure, ignore this municipality
				if "#" not in local_id:
					continue
				# report progress
				if verbose:
					os.system('cls')
					print(local_id)

				# put together URL and data
				local_data = {'Provincia': prov_id, 'Localidades': local_id}
				# get data for municipality and parse it
				local_response = BeautifulSoup(session.post(post_url, local_data).text, 'html.parser')
				# find all month table widgets
				months = local_response.findAll("table", {"class": "work-calendar"})
				for i, month in enumerate(months):
					month_name = month.find("caption").get_text()
					for day in month.findChildren("td"):
						# only holidays have an extra inner span to add coloring tags
						day_span = day.findChild("span")
						if day_span:
							date = datetime.strptime("{} {} {}".format(day_span.get_text(),
																				i+1,
																				self.current_year), "%d %m %Y")
							# extract province code and name
							prov_code, prov_name = (x.strip() for x in prov_id.split("#"))
							# extract local code and name
							local_code, local_name = (x.strip() for x in local_id.split("#"))
							# extract holiday tier and description
							holiday_type, holiday_description = [x.strip() for x in day.attrs["aria-label"].split(":")]

							# add holiday to list
							holidays.append(dict(province_name=prov_name.lower(),
												 province_cod=prov_code,
												 local_name=local_name.lower(),
												 local_cod=local_code,
												 date=date,
												 type=holiday_type,
												 description=holiday_description))

		# cast holidays to data-frame and return
		return pd.DataFrame(holidays)

	def list_provinces(self):
		return self.holidays["province_name"].unique().tolist()

	def list_municipalities(self):
		return self.holidays["local_name"].unique().tolist()
