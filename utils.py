import datetime

def aiyad(date, today=None):
    if today is None:
        today = datetime.date.today()
    year_diff = today.year - date.year
    if (today.month > date.month
        or today.month == date.month and today.day >= date.day):
        year_passed = 1
    else:
        year_passed = 0
    date_y = datetime.date(today.year + year_passed - 1, date.month, date.day)
    return (year_diff + year_passed - 1, (today - date_y).days)
        
