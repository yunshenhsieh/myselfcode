def bday(y,m):
    today=[2020,12]
    year_today=today[0];month_today=today[1]
    year_bday=y;month_bday=m
    month_vector = 12 - month_bday
    if year_today - year_bday >= 1:
        if month_vector + month_today >= 12:
            month = month_vector + month_today - 12
            year = year_today - year_bday
            return year,month
        else:
            month = month_vector + month_today
            year = year_today - year_bday - 1
            return year,month
    elif year_today - year_bday < 0:
        return False
    else:
        year = 0
        month = month_today - month_bday
        return year,month
