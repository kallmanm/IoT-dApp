from tkinter import *
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random

start_date = "2021-3-1"
stop_date = "2021-3-31"
start_time = "00:00:00"
stop_time = "23:59:59"


def mock_float():
    mf = round(random.uniform(0.00, 2.00), 2)
    return mf


def mock_db_output():
    db_output = (random_date(start_date, stop_date, random.random()),
                 random_time(start_time, stop_time, random.random()),
                 mock_float(), mock_float(), mock_float(),
                 mock_float(), mock_float(), mock_float(),
                 mock_float(), mock_float(), mock_float(),
                 mock_float())
    return db_output


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def random_time(start, end, prop):
    return str_time_prop(start, end, '%H:%M:%S', prop)


def make_many_entries(amount):
    data = []
    for i in range(amount):
        data.append(mock_db_output())
    return data


def transform_data_to_df(data, cols):
    df = pd.DataFrame(data, columns=cols)
    df['datetime'] = df['date'] + ' ' + df['time']
    df = df.drop(['date', 'time'], axis=1)
    df = df.sort_values(by="datetime")
    df = df.set_index('datetime')
    df.columns.name = 'measurements'
    return df


####################################
# Remove once eth connection works #
####################################


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("IoT-dApp")
        self.root.geometry("450x350")

        # DATA VAAR
        self.data = []

        # TEXT VARS
        self.keytext = StringVar()
        self.addresstext = StringVar()

        # LABEL VARS
        self.label1 = Label(self.root, textvariable=self.keytext)
        self.label2 = Label(self.root, textvariable=self.addresstext)

        # BUTTON VARS
        self.button1 = Button(self.root, text="Upload Key", command=self.upload_key)
        self.button2 = Button(self.root, text="Upload Address", command=self.upload_address)
        self.button3 = Button(self.root, text="Fetch Data", command=self.fetch_data)
        self.button4 = Button(self.root, text="Open Graph", command=self.pandas_graph)
        self.button5 = Button(self.root, text="Download Data", command=self.download_data)
        self.button6 = Button(self.root, text="Exit Program", command=self.root.quit)

        # SETTING ELEMENTS TO GRID
        self.button1.grid(row=0, column=0)
        self.button2.grid(row=1, column=0)
        self.button3.grid(row=2, column=0)
        self.button4.grid(row=3, column=0)
        self.button5.grid(row=4, column=0)
        self.button6.grid(row=5, column=0)
        self.label1.grid(row=0, column=1)
        self.label2.grid(row=1, column=1)

        # MAIN LOOP
        self.root.mainloop()

    def upload_key(self):
        filename = filedialog.askopenfilename()
        self.keytext.set(filename)
        # print(self.keytext.get()) to fetch variable data

    def upload_address(self):
        filename = filedialog.askopenfilename()
        self.addresstext.set(filename)

    # MODIFY TO SHOW DATA FROM MATCH SPS30
    def pandas_graph(self):
        # REPLACE WITH ACTUAL DATA SOURCE
        data = self.fetch_data()

        l1 = ["d1", "d2", "d3", "d4"]
        l2 = ["d5", "d6", "d7", "d8", "d9"]
        l3 = ["d10"]
        x = data.index
        frequency = 2
        rotation = 30
        title1 = "d1-d4"
        title2 = "d5-d9"
        title3 = "d10"
        padding = 2.5
        y1 = data[l1]
        y2 = data[l2]
        y3 = data[l3]

        plt.figure(figsize=[12, 8])

        plt.subplot(311)
        plt.plot(x, y1)
        plt.legend(l1)
        plt.xticks(np.arange(0, len(x) + 1, 5), rotation=rotation)
        plt.title(title1)

        plt.subplot(312)
        plt.plot(x, y2)
        plt.legend(l2)
        plt.xticks(np.arange(0, len(x) + 1, 5), rotation=rotation)
        plt.title(title2)

        plt.subplot(313)
        plt.bar(x, y3.d10)
        plt.legend(l3)
        plt.xticks(np.arange(0, len(x) + 1, 5), rotation=rotation)
        plt.title(title3)

        plt.tight_layout(pad=padding)
        plt.show()

    def fetch_data(self):
        # TODO: Make WEB3 py to fetch data and upload from csv for demo purpose.
        test = make_many_entries(30)
        cols = ['date', 'time', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10']
        df = transform_data_to_df(test, cols)

        # HOW TO GET PATH FROM VARS
        # OPEN FILES AND USE DATA TO ACCESS ETH
        # self.keytext.get()
        # self.addresstext.get()
        return df

    def download_data(self):
        # TODO: make pandas. to csv function download
        return None


app = App()
