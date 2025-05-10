# Path: lms/utils.py
def lect_time_to_sec(lect_time, mode):
    # mode 1. lect_time
    if mode=='end':
        lect_time = lect_time.split(" / ")[1]
    # mode 2. progress_time
    elif mode=='first':
        lect_time = lect_time.split(" / ")[0]

    # convert time to sec
    time_list = list(map(int, lect_time.split(":")))

    if len(time_list) == 3:
        h, m, s = time_list
        return h*3600 + m*60 + s
    elif len(time_list) == 2:
        m, s = time_list
        return m*60 + s