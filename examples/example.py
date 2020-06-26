from pyvacas import HolidaysCalendar


if __name__ == "__main__":
	cal = HolidaysCalendar()
	holidays = cal.get_holidays()
	print(holidays.shape)