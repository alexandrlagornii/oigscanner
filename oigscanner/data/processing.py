# Normalize data for doing OIG scans
def normalize_data_oig(data):
    """Given pandaframe with data, normalize it for usage in oig scans"""

    # Get columns
    columns = len(data.columns)

    # Normalize
    data = data.dropna()
    data = data.map(str)
    data = data.map(str.strip)

    # Normalize for individuals
    if (columns == 2):
        data = data.map(str.title)         

    # Print and return
    print(data)
    return data