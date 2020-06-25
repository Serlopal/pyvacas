import pytest
import pyvacas


@pytest.fixture(scope='session', autouse=True)
def calendar(request):
	return pyvacas.HolidaysCalendar()


def test_all_provinces(calendar):
	assert len(set(calendar.list_provinces())) >= 52


def test_unique_province_name_code_pairs(calendar):
	holidays = calendar.get_holidays()
	assert all([x == 1 for x in holidays.groupby("province_cod")["province_name"].nunique()])
	assert all([x == 1 for x in holidays.groupby("province_name")["province_cod"].nunique()])


def test_unique_local_name_code_pairs(calendar):
	holidays = calendar.get_holidays()
	assert all([x == 1 for x in holidays.groupby("local_cod")["local_name"].nunique()])
	assert all([x == 1 for x in holidays.groupby("local_name")["local_cod"].nunique()])


def test_three_holiday_types(calendar):
	holidays = calendar.get_holidays()
	assert holidays["type"].nunique() == 3
