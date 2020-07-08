from pyvacas.pyvacas import HolidaysCalendar


if __name__ == "__main__":
	cal = HolidaysCalendar()

	# locations = cal.get_locations(refresh_cache=True)

	holidays = cal.get_holidays(municipalities="ponferrada")

	# cal.re_scrape_data()

	print(holidays.head(5).to_string())
