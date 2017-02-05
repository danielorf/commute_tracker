

# Auto formats date values (month, day, hour, minute) to two digits - needed for proper date formatting by Plotly
def date_formatter(val):
    if val < 10:
        val = '{}{}'.format('0', str(val))
        return val
    elif val >= 10:
        return str(val)
    else:
        print('Improper date value formatting')
        print(val)