# PyVacas

A lightweight module that provides easy access to all national, regional and local holidays in Spain using a Pandas dataframe format.

## Installation

Install it from TestPyPI

```
pip install PyVacas --extra-index-url=https://test.pypi.org/simple/

```


## Usage

You can fetch all available holidays for Spain using ```get_holidays``` without any extra arguments

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar()
holidays = cal.get_holidays()
```

Or check out available provinces and municipalities using ```list_provinces``` or ```list_municipalities``` and provide them to
```get_holidays``` to retrieve only the holidays for the desired locations.

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar()
holidays = cal.get_holidays(provinces="Madrid")
```

You can provide a single item using a string or multiple ones in the form of lists. If you choose to provide both provinces and municipalities,
the holidays will be filtered so that they are coincident for both of them.


```HolidaysCalendar``` checks at creation time for the availability of holiday data already cached inside the library. If the data is not present,
the program will automatically start scrapping the data from the web. In case the data is present but the user wants to refresh it for any reason,
this can be done using the ```re_scrape_data``` method.

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar()
cal.re_scrape_data()
```