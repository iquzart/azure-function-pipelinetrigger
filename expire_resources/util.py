import tabulate


def tabulate_report(data):
    """
    Return tabulated values
    """    
    header = data[0].keys()
    rows =  [x.values() for x in data]
    return (tabulate.tabulate(rows, header))
    