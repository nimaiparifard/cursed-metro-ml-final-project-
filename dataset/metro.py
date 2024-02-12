import numpy as np
from dataset.station import Station
import datetime
import matplotlib.pyplot as plt
import networkx as nx
from dataset.stations import *
class Metro:
    def __init__(self) -> None:
        self.stations_list = []
        # Defining stations from the end of each line towards the beginning
        # Exit Stations
        kahrizak = Station(Kahrizak, input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        basij = Station(Basij, input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        ghaem = Station(Ghaem, input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        buali = Station(Booali, input_rate_range=(0, 0), output_rate_range=None, children=[], is_last_station=True)
        
        # Common and Normal Stations (defined in reverse order to correctly assign children)
        # Line 1
        mohammadiye = Station(Mohamadieh, input_rate_range=(10, 14), output_rate_range=(15, 20), children=[kahrizak], crowed_station=True)
        dowlat = Station(Dowlat, input_rate_range=(10, 14), output_rate_range=(15, 20), children=[mohammadiye], crowed_station=True)
        beheshti = Station(Beheshti, input_rate_range=(10, 14), output_rate_range=(15, 20), children=[dowlat])  # Shared with Line 3
        shariati = Station(Shariati, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[beheshti])
        tajrish = Station(Tajrish, input_rate_range=(30, 40), output_rate_range=(0, 0), children=[shariati], is_first_station=True, crowed_station=True)
        
        # Line 2
        molavi = Station(Molavi, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[basij])
        # Mohammadiye already defined, add Molavi as a child
        mohammadiye.children.append(molavi)
        teatr = Station(Theather, input_rate_range=(10, 14), output_rate_range=(15, 20), children=[mohammadiye], crowed_station=True)  # Shared with Line 4
        valiasr = Station(Valiasr, input_rate_range=(10, 14), output_rate_range=(15, 20), children=[teatr], crowed_station=True)  # Shared with Line 3
        sanat = Station(Sanat, input_rate_range=(30, 40), output_rate_range=(0, 0), children=[valiasr], is_first_station=True)
        
        # Line 3
        heravi = Station(Heravi, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[ghaem])
        # Beheshti already defined, add Heravi as a child
        beheshti.children.append(heravi)
        jihad = Station(Jahad, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[beheshti])
        # Valiasr already defined, add Jihad as a child
        valiasr.children.append(jihad)
        sattari = Station(Sattari, input_rate_range=(30, 40), output_rate_range=(0, 0), children=[valiasr], is_first_station=True)
        
        # Line 4
        shemiran = Station(Shemiran, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[buali])
        ferdowsi = Station(Ferdowsi, input_rate_range=(10, 14), output_rate_range=(8, 12), children=[shemiran])
        # Teatr already defined, add Ferdowsi as a child
        teatr.children.append(ferdowsi)
        azadi = Station(Azadi, input_rate_range=(30, 40), output_rate_range=(0, 0), children=[teatr], is_first_station=True)
        
    
        # Store all stations in a list or dictionary for further processing if needed
        self.stations = {
            Kahrizak: kahrizak, Basij: basij, Ghaem: ghaem, Booali: buali,
            Mohamadieh: mohammadiye, Dowlat: dowlat, Beheshti: beheshti,
            Shariati: shariati, Tajrish: tajrish, Molavi: molavi, Theather: teatr,
            Valiasr: valiasr, Sanat: sanat, Heravi: heravi, Jahad: jihad,
            Sattari: sattari, Shemiran: shemiran, Ferdowsi: ferdowsi, Azadi: azadi
        }

        for station_name, station_object in self.stations.items():
            self.stations_list.append(station_object)

        self.lines = {
            'Line1' : Line1,
            'Line2' : Line2,
            'Line3' : Line3,
            'Line4' : Line4
        }

    def create_metro_graph(self):
        metro_structure = {
            Kahrizak: [],
            Basij: [],
            Ghaem: [],
            Booali: [],
            Mohamadieh: [Kahrizak, Molavi],
            Dowlat: [Mohamadieh],
            Beheshti: [Dowlat, Heravi],
            Shariati: [Beheshti],
            Tajrish: [Shariati],
            Molavi: [Basij],
            Theather: [Mohamadieh, Ferdowsi],
            Valiasr: [Theather, Jahad],
            Sanat: [Valiasr],
            Heravi: [Ghaem],
            Jahad: [Beheshti],
            Sattari: [Valiasr],
            Shemiran: [Booali],
            Ferdowsi: [Shemiran],
            Azadi: [Theather],
        }
        # Create a directed graph from the metro structure
        G = nx.DiGraph(metro_structure)
        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(18, 10))
        nx.draw(G, pos, with_labels=True, node_size=2500, node_color='skyblue', font_size=10, font_weight='bold', arrowstyle='-|>', arrowsize=12)
        plt.title('Metro Station Structure (Improved Layout)')
        plt.axis('off')  # Turn off the axis for a cleaner look
        plt.show()



    def metro_simulation_one_day(self):
        # Start time: 6 AM on 1st Jan 2024
        start_time = datetime.datetime(2024, 1, 1, 6, 0)
        # End time: 10 PM on the same day
        end_time = datetime.datetime(2024, 1, 1, 22, 0)
        
        # Current simulation time
        timestamp = start_time
        
        while timestamp <= end_time:
            print(f"Simulating for time: {timestamp}")  # Placeholder for simulation steps
            
            # Loop through each line in sequence
            for line_name, stations in self.lines.items():  # Assuming self.lines is defined in __init__
                print(f"Processing {line_name}")  # Placeholder for line processing
                current_passenger = 0
                line_timestamp = timestamp
                for station_name in stations:
                    station = self.stations[station_name]
                    station.set_current_in_train_passenger(current_passenger)
                    station.set_line_number_rate(line_name)
                    station.set_crowed_station_rate()
                    station.set_crowed_time_rate(timestamp)
                    station.is_holiday(0)
                    station.is_weekend(0)
                    station.generate_input_rate()
                    station.generate_output_rate()
                    current_passenger = current_passenger + station.input_rate - station.output_rate
                    # Simulate passenger flow at this station
                    station.passengers_flow(timestamp)
                    line_timestamp += datetime.timedelta(minutes=6)
                    print(f"Simulated passengers flow at {station.name}")  # Placeholder for actual simulation
                    
            # Increment timestamp by 6 minutes
            timestamp += datetime.timedelta(minutes=30)
            
        print("Simulation complete.")


cursed_metro = Metro()
cursed_metro.create_metro_graph()
cursed_metro.metro_simulation_one_day()