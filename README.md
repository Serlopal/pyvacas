# PyVacas

A lightweight module that provides easy access to all national, regional and local holidays in Spain using a Pandas dataframe format.

## Installation

Just clone the repo to your local project and make sure you install the Python dependencies with

```
pip install -r requirements.txt
```


The module already includes the holidays for 2020 cashed into it.If you want to re-scrape the data, just do:

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar()
holidays = cal.load_holidays(re_scrape=True)
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
