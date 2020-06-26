from pyvacas import HolidaysCalendar


if __name__ == "__main__":
	cal = HolidaysCalendar()

	print(cal.list_provinces())
	print(cal.list_municipalities())

	holidays = cal.get_holidays(municipalities=["PONFERRADA", "VALLADOLID"])
	print(holidays.head(500).to_string())
