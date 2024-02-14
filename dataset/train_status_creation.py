import numpy as np
import pandas as pd
from stations import *
import datetime
import csv

def creating_train_status_dataset():
    start_time = datetime.datetime(2024, 1, 1, 6, 0)
    # End time: 10 PM on the same day
    end_time = datetime.datetime(2024, 1, 1, 21, 30)

    # Current simulation time
    timestamp = start_time
    train_number = 0

    while timestamp <= end_time:
        print(f"Simulating for Holiday time: {timestamp}")  # Placeholder for simulation steps

        # Loop through each line in sequence
        train_number += 1
        for line_name, stations in Lines.items():  # Assuming self.lines is defined in __init__
            print(f"Processing {line_name}")  # Placeholder for line processing
            current_passenger = 0
            line_timestamp = timestamp
            for station_name in stations:
                station_number_in_line, line_number = get_station_number_in_line(station_name, line_name)
                # if station_number_in_line == 1:
                train_number_ = str(line_number) + "_" + str(train_number)
                next_station_arrived =line_timestamp + datetime.timedelta(minutes=6)
                next_station = station_number_in_line + 1
                if station_number_in_line == 6:
                    next_station = 0
                    next_station_arrived = 0

                with open('train_status.csv', 'a', newline='') as file:
                    writer = csv.writer(file)

                    if file.tell() == 0:
                        writer.writerow((['train_number', 'line_number', 'current_timestamp','current_station', 'current_passenger', 'next_station',
                                          'next_station_time_arrived']))

                    writer.writerow(
                        [train_number_,line_number,line_timestamp,station_number_in_line, 0, next_station, next_station_arrived])
                line_timestamp += datetime.timedelta(minutes=6)
        timestamp += datetime.timedelta(minutes=6)

def get_station_number_in_line(station_name, line_name):
    if line_name == 'Line1':
        station_number = Line1.index(station_name)
        return station_number + 1, 1
    elif line_name == 'Line2':
        station_number = Line2.index(station_name)
        return station_number + 1, 2
    elif line_name == 'Line3':
        station_number = Line3.index(station_name)
        return station_number + 1, 3
    else:
        station_number = Line4.index(station_name)
        return station_number + 1, 4

creating_train_status_dataset()