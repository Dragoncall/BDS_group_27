import datetime
import json
from os import listdir
from os.path import isfile, join, dirname, realpath

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting._matplotlib.converter import TimeSeries_TimedeltaFormatter, TimeSeries_DateFormatter

DATA_TROVE_PATH = "/Users/Karel/PycharmProjects/BDS_group_27/data_trove"  # Change this to your own directory
dir_path = dirname(realpath(__file__))


RECENT = 'recent'
POPULAR = 'popular'

TYPES = ['Positive', 'Negative', 'Neutral']

def read_time_data_for_person(handle, type):
    files = []
    for file in listdir(DATA_TROVE_PATH):
        full_path = join(DATA_TROVE_PATH, file)
        if not isfile(full_path):
            continue
        if handle in full_path and type in full_path:
            files.append(full_path)

    dict_list = []
    indices = []
    for file in files:
        with open(file, 'r') as f:
            json_dict = json.load(f)
            for TYPE in TYPES:
                json_dict[TYPE] = json_dict.get(TYPE, None) or 0
            dict_list.append(json_dict)

        # indices.append(pd.to_datetime(file.split('/')[-1].split('_')[-2]))
        # indices.append(datetime.datetime.strptime(, '%Y-%m-%d %H:%M:%S.%f'))
        # date = pd.to_datetime(file.split('/')[-1].split(' ')[0].split('_')[-1])
        date = file.split('/')[-1].split('.')[0].split('_')[2:]
        date = ':'.join(date)
        indices.append(date)

    df = pd.DataFrame(dict_list, index=indices)
    return df

def plot_time_data(df:pd.DataFrame, title):
    if len(df) == 0:
        print(f'Empty dataframe for title: {title}')
        return

    ax = df.plot(
        None, ['Negative', 'Neutral', 'Positive'],
        'area', stacked=True,
        color=['#fc8d59', '#ffffbf', '#91cf60'],
        title=title
    )
    # format_x_date_month_day(ax)
    plt.show()

def get_all_handles():
    with open(f'{dir_path}/../../resources/prominent_people.json', 'r') as f:
        return json.load(f).keys()

if __name__ == '__main__':
    for handle in get_all_handles():
        df = read_time_data_for_person(handle, POPULAR)
        plot_time_data(df, title=handle)





