#
#   PROJECT : Simulation of a Single Server Queue
# 
#   FILENAME : main.py
# 
#   DESCRIPTION :
#       The objective is to simulate a single server queue system and understand
#       the effect of processing delay on the system.
# 
#   FUNCTIONS :
#       main()
# 
#   NOTES :
#       ...
# 
#   AUTHOR(S) : Noah Arcand Da Silva    START DATE : 2022.10.11 (YYYY.MM.DD)
#
#   CHANGES :
#       - ...
# 
#   VERSION     DATE        WHO             DETAILS
#   0.0.1a      2022.10.11  Noah            Creation of project.
#


import time


# Class that contains all of our data arrays.
class SimData:
    inter_arrival_time = []
    service_time_mu3 = []
    service_time_mu5 = []
    service_time_mu6 = []
    service_time_mu8 = []

    # Initialize data lists from given text files.
    def __init__(self):
        # Store inter-arrival time data to list.
        with open("./interArrivals.txt") as file:
            for line in file:
                line = float(line.strip())
                self.inter_arrival_time.append(line)
        # Store service time data with a service rate of 3 packets/sec to list.
        with open("./serviceTimesMu3.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu3.append(line)
        # Store service time data with a service rate of 5 packets/sec to list.
        with open("./serviceTimesMu5.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu5.append(line)
        # Store service time data with a service rate of 6 packets/sec to list.
        with open("./serviceTimesMu6.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu6.append(line)
        # Store service time data with a service rate of 8 packets/sec to list.
        with open("./serviceTimesMu8.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu8.append(line)


# Class that does the simulation.
class Simulation:
    inter_arrival_time = []
    service_time = []
    clock_arrival_time = []
    queue_delay = []
    depature_time = []
    total_waiting_time = []

    # Simulation of router with a single server queue with infinite buffer.
    def simulation(self, service_rate=8, queue_size=1, buffer=0):
        s = SimData()
        # Set the service rate which we want to simulate.
        if (service_rate == 3):
            self.service_time = s.service_time_mu3
        elif (service_rate == 5):
            self.service_time = s.service_time_mu5
        elif (service_rate == 6):
            self.service_time = s.service_time_mu6
        else:
            self.service_time = s.service_time_mu8


# Class that collects statistical data.
class SimStats:
    def __init__():
        pass

    def get_arrival_rate(self, service_rate):
        pass


# Main function
def main():
    sim = Simulation()
    sim.simulation(service_rate=3, queue_size=1, buffer=0)

# Execution of the code
if __name__ == "__main__":
    main()