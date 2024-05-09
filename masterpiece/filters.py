def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
    if value:
        return value.strftime(fmt)

def round2(value):
    if value:
        return round(value, 2)