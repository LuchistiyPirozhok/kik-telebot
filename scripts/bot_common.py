import time


def get_timestamp():
    '''
    Returns time passed from 01.01.1970 in minutes
    '''

    return int(time.time()/60)
