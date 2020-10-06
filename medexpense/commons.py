def normalize_cellphone(value):
    if value is None:
        return value
    string = ''.join([v for v in str(value) if v.isdigit()])
    if string[0] != '0':
        string = f"{str(0)}{string}"
    return string