import numpy as np
import logging
import csv
logging.basicConfig(filename='stations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Station:
    def __init__(self,name,input_rate_range,output_rate_range,children:list["Station"],is_last_station=False,is_first_station=False, current_in_train_passenger=0, crowed_station=False) -> None:
        self.name = name
        self.passengers = 0
        self.input_rate_range = input_rate_range
        self.output_rate_range = output_rate_range
        self.children = children
        self.is_last_station = is_last_station
        self.is_first_station = is_first_station
        self.current_in_train_passenger = current_in_train_passenger
        self.crowed_station = crowed_station
        self.holiday = 0
        self.weekend = 0
    
    def generate_input_rate(self): # these people came from outsied of the metro rate ...
        input_rate =  int(np.random.poisson(np.random.randint(self.input_rate_range[0], self.input_rate_range[1]+1)) * self.line_number_rate * self.crowed_rate *
                          self.weekend_rate * self.holiday_rate * self.crowed_station_rate)
        if self.is_last_station:
            input_rate = 0
        logging.info(f'the input (from out of the metro) into the station {self.name} is : {input_rate}')
        self.input_rate = input_rate

    def set_line_number_rate(self, line_number):
        self.line_number = line_number
        if self.line_number == 'Line1' and self.line_number == 'Line2':
            self.line_number_rate = 1.2
        else:
            self.line_number_rate = 1

    def set_crowed_time_rate(self, timestamp):
        if timestamp.hours > 6 and timestamp.hours < 8:
            self.crowed_rate = 0.8
        elif timestamp.hours >= 8 and timestamp.hours < 12:
            self.crowed_rate = 1.2
        elif timestamp.hours >= 12 and timestamp.hours < 16:
            self.crowed_rate = 1
        elif timestamp.hours >= 16 and timestamp.hours < 20:
            self.crowed_rate = 1.2
        else:
            self.crowed_rate = 0.8

    def is_weekend(self, weekend):
        self.weekend = 1
        if weekend:
            self.weekend_rate = 0.8
        self.weekend_rate = 1
    def is_holiday(self, holiday):
        self.holiday = 1
        if holiday:
            self.holiday_rate = 0.4
        self.holiday_rate = 1
    def set_crowed_station_rate(self):
        if self.crowed_station:
            self.crowed_station_rate = 1.8
        self.crowed_station_rate = 1

    def generate_output_rate(self): # these people leave the metro rate ....
        if self.is_first_station:
            output_rate = 0
        elif self.is_last_station:
            output_rate = self.current_in_train_passenger
            logging.info(f'END OF THE LINE: the output (leaving the metro) from the station {self.name} is : {output_rate}')
        else:
            output_rate = int(np.random.poisson(np.random.randint(self.input_rate_range[0], self.input_rate_range[1]+1)) * self.line_number_rate * self.crowed_rate *
                          self.weekend_rate * self.holiday_rate * self.crowed_station_rate)
            if output_rate > self.current_in_train_passenger:
                output_rate = self.current_in_train_passenger
            logging.info(f'the output (leaving the metro) from the station {self.name} is : {output_rate}')
        self.output_rate = output_rate

    def set_current_in_train_passenger(self, train_passenger):
        self.current_in_train_passenger = train_passenger

    def passenger_departed(self): # this function have to be very carefully executed because it has to be after the other functions ...
        if len(self.children) != 0:
            for child in self.children:
                child.passengers += (self.passengers / len(self.children)) # the currnet (remaining) passengers are divided by the number of possible next station
            self.passengers = 0

    def passengers_flow(self, timestamp):
        print(f'passenger flow started for {self.name}')
        self.passengers += self.input_rate

        # step 2: the passengers which leaves the metro through this station ....
        self.passengers -= self.output_rate
        logging.info(f'current people in the metro: {self.current_in_train_passenger + self.input_rate - self.output_rate}')
        # Open or create the CSV file in append mode
        with open('metro_passenger_flow.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Check if file is empty to write headers
            if file.tell() == 0:
                writer.writerow(['timestamp', 'station_name', 'input_count', 'output_count', 'current_in_line_passengers', 'line_number', 'crowed_time_rate', 'is_crowed_station', 'is_weekend', 'is_holiday'])
            # Write the data row
            writer.writerow([timestamp, self.name, self.input_rate, self.output_rate, self.current_in_train_passenger, self.line_number, self.crowed_rate, self.crowed_station, self.weekend, self.holiday])

        if self.passengers < 0:
            logging.info('The number of passengers became negative at {}'.format(self.name))
            self.passengers = 0

        # step 3: the passengers will then be divided by the possible number of stations and ....
        self.passenger_departed()