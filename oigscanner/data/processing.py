import pandas as pd 


def normalize_data_oig(data: pd.DataFrame) -> pd.DataFrame:
    """Given pandas dataframe with data, normalize it for usage in oig scans.
    
    Args:
        data: pandas dataframe with either two columns or one

    Returns:
        Pandas dataframe with normalized data
    """
    assert len(data.columns) == 1 or len(data.columns) == 2

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