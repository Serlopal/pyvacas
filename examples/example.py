from pyvacas import HolidaysCalendar


if __name__ == "__main__":
	cal = HolidaysCalendar()
	# cal.load_holidays(re_scrape=True)

	print(cal.list_provinces())
	print(cal.list_municipalities())

	holidays = cal.get_holidays(provinces="madrid", municipalities="alcobendas")
	print(holidays.head(500).to_string())
