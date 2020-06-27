from pyvacas import HolidaysCalendar


if __name__ == "__main__":
	cal = HolidaysCalendar()

	locations = cal.get_locations()

	holidays = cal.get_holidays(municipalities="ponferrada")

	print("asd")
