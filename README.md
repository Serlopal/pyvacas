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

```python
from pyvacas import HolidaysCalendar

cal = HolidaysCalendar()
holidays = cal.get_holidays()
```
