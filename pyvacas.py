from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
from datetime import datetime
import pandas as pd
import os
import pickle
from functools import wraps

package_directory = os.path.dirname(os.path.abspath(__file__))


class HolidaysCalendar:
	def __init__(self):
		self.base_url = "http://www.seg-social.es/wps/portal/wss/internet/CalendarioLaboral"
		self.current_year = datetime.now().year
		self.municipalities_dropdown = "provinciasLocalidades"
		self.html_session = HTMLSession()

		self.cache_path = os.path.join(package_directory, "cache")

		self.endpoint_path = os.path.join(self.cache_path, "endpoint.pkl")
		self.endpoint_ready = False
		self.endpoint = None

		self.locations_path = os.path.join(self.cache_path, "locations.pkl")
		self.locations_ready = False
		self.locations = None

		self.holidays_path = os.path.join(self.cache_path, "holidays.pkl")
		self.holidays_ready = False
		self.holidays = None

		self._check_cache_ready()

	def _cache(name):
		"""
		decorator that will save the result of the function it wraps in the cache as a pickle file.
		:param name: name of the file to be saved in the cache

		"""

		def _decorator(f):
			def wrapper(self, *args, **kwargs):
				f(self, *args, **kwargs)
				# write to cache
				r = getattr(self, name)
				try:
					with open(os.path.join(self.cache_path, "{}.pkl".format(name)), 'wb') as h:
						pickle.dump(r, h)
				except:
					raise Exception("Could not write {} to cash".format(name))

			return wrapper

		return _decorator

	def _scrape_if_not_ready(*required):
		"""
		decorator that will wrap methods that use cache resources and rescrape them if not available.
		:param required: list of resources required by the wrapped function
		"""
		def _decorator(f):
			def wrapper(self, *args, **kwargs):
				for req in required:
					if not getattr(self, "{}_ready".format(req)):
						print("{} not found, scrapping...".format(req))
						getattr(self, "scrape_{}".format(req))()

				return f(self, *args, **kwargs)

			return wrapper

		return _decorator

	@property
	def _scraping_ready(self):
		"""
		Checks we have found the URL of the endpoint and the province-municipality combos available.
		These two resources are necessary to start scraping the holiday data.
		"""
		return self.endpoint_ready and self.locations_ready

	def _check_cache_ready(self):
		"""
		Checks the availability in the cache of:
			- the endpoint URL
			- the province-municipality combinations for the endpoint
			- the full holiday data
		"""
		# check real endpoint URL is stored in disk
		if os.path.exists(self.endpoint_path):
			self.endpoint_ready = True
			self.endpoint = pd.read_pickle(self.endpoint_path)

		# check list of available locations is stored in disk
		if os.path.exists(self.locations_path):
			self.locations_ready = True
			self.locations = pd.read_pickle(self.locations_path)

		# check holidays table is stored in disk
		if os.path.exists(self.holidays_path):
			self.holidays_ready = True
			self.holidays = pd.read_pickle(self.holidays_path)

	@_cache("endpoint")
	def scrape_endpoint(self):
		"""

		:return:
		"""
		soup = BeautifulSoup(self.html_session.get(self.base_url).text, 'html.parser')
		action = soup.find('form', id=self.municipalities_dropdown).get('action')
		real_url = soup.find("base")["href"]
		self.endpoint = "{}{}".format(real_url, action)

	@_cache("locations")
	def scrape_locations(self):
		"""
		Scrapes all available province-municipality combinations .
		"""
		soup = BeautifulSoup(self.html_session.get(self.base_url).text, 'html.parser')
		# get all province ids available
		provinces_ids = [x["value"] for x in soup.find("select", id="Provincia").findChildren("option", recursive=False)]

		# temporal dictionary to store all province-municipality combinations
		d = dict()

		for i, prov_id in enumerate(provinces_ids):
			print(prov_id)
			# put together URL and data
			prov_data = {'Provincia': prov_id}
			# get data with POST method
			regional_response = BeautifulSoup(self.html_session.post(self.endpoint, prov_data).text, 'html.parser')
			# get all location ids in the province
			municipalities_html = regional_response.find("select", id="Localidades")
			# if there are not any municipalities, go to the next region
			if not municipalities_html:
				continue
			# extract the municipality ids
			municipality_ids = [x["value"] for x in municipalities_html.findChildren("option", recursive=False)]

			# add to dict
			d[prov_id] = municipality_ids

		self.locations = d

	@_cache("holidays")
	def scrape_holidays(self, verbose=True):
		"""
		Scrapes all available holiday data for all locations.
		:param verbose: if True, the municipality being scrapped will be printed
		"""
		holidays = []
		for prov, municipalities in self.locations.items():
			for mun in municipalities:
				# if no cod#name structure, ignore this municipality
				if "#" not in mun:
					continue
				# report progress
				if verbose:
					os.system('cls')
					print(mun)

				# put together URL and data
				local_data = {'Provincia': prov, 'Localidades': mun}
				# get data for municipality and parse it
				local_response = BeautifulSoup(self.html_session.post(self.endpoint, local_data).text, 'html.parser')
				# find all month table widgets
				months = local_response.findAll("table", {"class": "work-calendar"})
				for i, month in enumerate(months):
					month_name = month.find("caption").get_text()
					for day in month.findChildren("td"):
						# only holidays have an extra inner span to add coloring tags
						day_span = day.findChild("span")
						if day_span:
							holidays.append(self._format_holiday(day_span.get_text(), i + 1, prov, mun, day.attrs["aria-label"]))
		# save holidays to data-frame
		self.holidays = pd.DataFrame(holidays)

	def _format_holiday(self, day, month, province, municipality, description):
		"""
		function that receives scrapped data and formats it into a dictionary representing all info for a holiday
		:param day: day of the month
		:param month: month of the year
		:param province: province id containing the province name and code
		:param municipality: municipality id containing the municipality name and code
		:param description: description of the holiday
		:return: dictionary with the final holiday description
		"""
		date = datetime.strptime("{} {} {}".format(day, month, self.current_year), "%d %m %Y")
		# extract province code and name
		prov_code, prov_name = (x.strip() for x in province.split("#"))
		# extract local code and name
		local_code, local_name = (x.strip() for x in municipality.split("#"))
		# extract holiday tier and description
		holiday_type, holiday_description = [x.strip() for x in description.split(":")]

		# add holiday to list
		return dict(province_name=prov_name.lower(),
					province_cod=prov_code,
					local_name=local_name.lower(),
					local_cod=local_code,
					date=date,
					type=holiday_type,
					description=holiday_description)

	@_scrape_if_not_ready("endpoint", "locations")
	def get_locations(self):
		"""
		Returns a dictionary that contains all availables municipalities for each available province
		"""
		return self.locations

	@_scrape_if_not_ready("endpoint", "locations", "holidays")
	def get_holidays(self, provinces=None, municipalities=None):
		"""
		Returns a pandas DataFrame containing all available holiday info if no arguments are specified,
		or holiday info for the required locations in case a filter is specified.
		:param provinces: list or string containing one or multiple provinces to get holidays for
		:param municipalities: list or string containing one or multiple municipalities to get holidays for
		:return: pandas DataFrame with holiday data
		"""

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









