# PyVacas

A lightweight module that provides easy access to all national, regional and local holidays in Spain using a Pandas dataframe format.

## Installation

Just clone the repo to your local project. It's light weight and already includes the holidays for 2020 cashed into the module.

If you want to re-scrape the data, just do

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar
holidays = cal.load_holidays(re_scrape=True)
```


## Usage

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar
holidays = cal.get_holidays()
```
