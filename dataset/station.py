import numpy as np
import logging
import csv
logging.basicConfig(filename='stations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Station:
    def __init__(self,name,input_rate_range,output_rate_range,children:list["Station"],is_last_station=False,is_first_station=False) -> None:
        self.name = name
        self.passengers = 0
        self.input_rate_range = input_rate_range
        self.output_rate_range = output_rate_range
        self.children = children
        self.is_last_station = is_last_station
        self.is_first_station = is_first_station
    
    def generate_input_rate(self): # these people came from outsied of the metro rate ...
        input_rate =  np.random.poisson(np.random.randint(self.input_rate_range[0], self.input_rate_range[1]+1))
        logging.info(f'the input (from out of the metro) into the station {self.name} is : {input_rate}')
        return input_rate
    
    def generate_output_rate(self): # these people leave the metro rate ....
        if self.is_last_station:
            output_rate = self.passengers
            logging.info(f'END OF THE LINE: the output (leaving the metro) from the station {self.name} is : {output_rate}')
        else:
            output_rate = np.random.poisson(np.random.randint(self.output_rate_range[0], self.output_rate_range[1]+1))
            logging.info(f'the output (leaving the metro) from the station {self.name} is : {output_rate}')
        return output_rate
    
    def passenger_departed(self): # this function have to be very carefully executed because it has to be after the other functions ...
        if len(self.children) != 0:
            for child in self.children:
                child.passengers += (self.passengers / len(self.children)) # the currnet (remaining) passengers are divided by the number of possible next station
            self.passengers = 0

    def passengers_flow(self, timestamp):
        print(f'passenger flow started for {self.name}')
        # step 1: the passengers which enters the metro through this station ...
        entered = self.generate_input_rate()
        self.passengers += entered

        # step 2: the passengers which leaves the metro through this station ....
        leaved = self.generate_output_rate()
        self.passengers -= leaved

        # Open or create the CSV file in append mode
        with open('metro_passenger_flow.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Check if file is empty to write headers
            if file.tell() == 0:
                writer.writerow(['timestamp', 'station_name', 'input_count', 'output_count'])
            # Write the data row
            writer.writerow([timestamp, self.name, entered, leaved])

        if self.passengers < 0:
            logging.info('The number of passengers became negative at {}'.format(self.name))
            self.passengers = 0

        # step 3: the passengers will then be divided by the possible number of stations and ....
        self.passenger_departed()