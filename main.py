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
#       The simulation took a bit of work to determine the best, most appropriate
#       equations to use for each simulation variable.
# 
#   AUTHOR(S) : Noah Arcand Da Silva    START DATE : 2022.10.11 (YYYY.MM.DD)
#
#   CHANGES :
#       - ...
# 
#   VERSION     DATE        WHO             DETAILS
#   0.0.1a      2022.10.11  Noah            Creation of project.
#   0.0.1b      2022.10.12  Noah            First functional version of program.
#


import matplotlib.pyplot as plt


# Class that contains all of our data arrays.
class SimulationInputData:
    inter_arrival_time = []
    service_time_mu3 = []
    service_time_mu5 = []
    service_time_mu6 = []
    service_time_mu8 = []

    # Initialize data lists from given text files.
    def __init__(self):
        # Store inter-arrival time data to list.
        with open("interArrivals.txt") as file:
            for line in file:
                line = float(line.strip())
                self.inter_arrival_time.append(line)
        # Store service time data with a service rate of 3 packets/sec to list.
        with open("serviceTimesMu3.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu3.append(line)
        # Store service time data with a service rate of 5 packets/sec to list.
        with open("serviceTimesMu5.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu5.append(line)
        # Store service time data with a service rate of 6 packets/sec to list.
        with open("serviceTimesMu6.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu6.append(line)
        # Store service time data with a service rate of 8 packets/sec to list.
        with open("serviceTimesMu8.txt") as file:
            for line in file:
                line = float(line.strip())
                self.service_time_mu8.append(line)


# Class that does the simulation.
class Simulation:
    def __init__(self):
        self.sid = SimulationInputData()
        self.inter_arrival_time = self.sid.inter_arrival_time

    def set_service_rate(self, service_rate):
        self.service_rate = service_rate

    def get_service_rate(self):
        return self.service_rate    
    
    # Sets the appropriate service time list, depending on wanted service rate.
    def set_service_time_list(self, service_rate):
        if (service_rate == 3):
            self.service_time = self.sid.service_time_mu3
        elif (service_rate == 5):
            self.service_time = self.sid.service_time_mu5
        elif (service_rate == 6):
            self.service_time = self.sid.service_time_mu6
        else:
            self.service_time = self.sid.service_time_mu8
    
    def get_service_time_list(self):
        return self.service_time

    def get_arrival_rate(self, service_rate):
        return len(self.service_time) \
            / self.total_arrival_time()

    def total_arrival_time(self):
        total_time = 0
        for i in self.inter_arrival_time:
            total_time += i
        return total_time

    # Simulation of router with a single server queue with infinite buffer.
    # NOTE  BUFFER:         System capacity (How many packets are allowed to wait)
    #       QUEUE SIZE:     Amount of queues for packets to be processed.
    #       SERVICE RATE:   How many packets can be serviced per second.
    def simulate(self, service_rate=8, queue_size=1, buffer=0):
        # Since the first packet does not have an inter-arrival time, we need to initialize it
        # before we start the packet loop/simulation.
        clock_arrival_time = [0.0]
        queue_delay = [0.0]
        depature_time = [self.service_time[0]]
        total_waiting_time = 0.0

        time_service_begins = [0.0]
        time_spent_in_system = [self.service_time[0]]
        idle_time_of_server = [0.0]
        total_idle_time = 0.0
        total_spent_in_system = self.service_time[0]

        # Get the wanted 'service time' data set
        self.set_service_time_list(service_rate)

        for i in range(1, len(self.service_time)):
            # Let's calculate the arrival time on clock.
            # Add the previous packet's clock time to the arrive time of the current packet.
            clock_arrival_time.append(self.inter_arrival_time[i - 1] + clock_arrival_time[i - 1])

            # Let's increment the 'depature time' counter. Store in list.
            if depature_time[i - 1] > clock_arrival_time[i]:
                # If there is queue, we start from the departure of the previous packet.
                depature_time.append(depature_time[i-1] + self.service_time[i])
            else:
                # If there is no queue, we start from the arrival time of the packet.
                depature_time.append(clock_arrival_time[i] + self.service_time[i])
            
            # Let's calculate the queue delay.
            if (depature_time[i - 1] - clock_arrival_time[i]) >= 0:
                # If there is a queue, add it to the list.
                queue_delay.append(depature_time[i - 1] - clock_arrival_time[i])
            else:
                # If not, do not count negative values.
                queue_delay.append(0)

            # Let's increment the 'service time begins' counter. Store in list.
            time_service_begins.append(queue_delay[i] + clock_arrival_time[i])

            # Let's calculate the idle time of the server.
            if (time_service_begins[i] - depature_time[i - 1]) >= 0:
                idle_time_of_server.append(time_service_begins[i] - depature_time[i - 1])
            else:
                # Makes sure we don't have any negative values.
                idle_time_of_server.append(0)
                #idle_time_of_server.append((time_service_begins[i] - depature_time[i - 1]) * (-1))

            # Let's calculate the time spent in the system.
            time_spent_in_system.append(queue_delay[i] + self.service_time[i])

            # Add up the waiting time of every packet.
            total_waiting_time += queue_delay[i]
            # Add up time spent in system of every packets.
            total_spent_in_system += time_spent_in_system[i]
            # Add up the idle time of the system.
            total_idle_time += idle_time_of_server[i]
        
        # Return all of our data
        return  clock_arrival_time,     \
                time_service_begins,    \
                queue_delay,            \
                depature_time,          \
                time_spent_in_system,   \
                idle_time_of_server,    \
                total_waiting_time,     \

    def graph_plot(self, data, plot_title):
        # We want the packet number, i.e. 1, 2, 3, ...
        x_axis = [i for i in range(1, len(data) + 1)]
        # Create a bar graph for queuing delay of packets.
        plt.clf()
        plt.style.use('ggplot')
        plt.bar(x_axis, data, width=1, color='cornflowerblue')
        # Formatting 
        plt.title(plot_title)
        plt.xlabel('Packet number')
        plt.ylabel('Queueing delay (seconds)')
        plt.savefig('histograms/' + plot_title + '.png')

    def average_queuing_delay(self, queue_delay):
        total_qd = 0
        for i in queue_delay:
            total_qd += i
        return total_qd / len(queue_delay)


    def average_time_spent_in_system(self, time_spent_in_system):
        total_tsis = 0
        for i in time_spent_in_system:
            total_tsis += i
        return total_tsis / len(time_spent_in_system)
        
    def waiting_probability(self, queue_delay):
        num_waiting_packets = 0
        for i in queue_delay:
            if i != 0:
                num_waiting_packets += 1
        return num_waiting_packets / len(queue_delay)

    def average_number_of_packets_in_system(self, total_waiting_time, departure_time):
        simulation_time = departure_time[-1]
        return total_waiting_time / simulation_time

    def print_sim_data(self, sim_results):
        print("Average Queueing Delay:\t\t\t" + 
            str(self.average_queuing_delay(sim_results[2])))
        print("Average Time Spent In System:\t\t" + 
            str(self.average_time_spent_in_system(sim_results[4])))
        print("Waiting Probability of Packet:\t\t" + 
            str(self.waiting_probability(sim_results[2])))
        print("Average Num of Packets in System:\t" + 
            str(self.average_number_of_packets_in_system(sim_results[6], sim_results[3])))


# Main function
def main():
    SERVICE_RATE = 8
    QUEUE_SIZE = 1
    BUFFER = 0
    s = Simulation()
    s.set_service_rate(service_rate=SERVICE_RATE)
    s.set_service_time_list(s.get_service_rate)
    
    print("\nThe average arrival rate for packets is " \
        + str(s.get_arrival_rate(service_rate=SERVICE_RATE)) + " per second.")

    print("\nSERVICE RATE OF 3 PACKETS PER SECOND \n")
    SERVICE_RATE = 3
    sim_results = s.simulate(service_rate=SERVICE_RATE, queue_size=QUEUE_SIZE, buffer=BUFFER)
    s.graph_plot(sim_results[2], "Queueing delay of each packet (service rate of 3)")
    s.print_sim_data(sim_results=sim_results)

    print("\nSERVICE RATE OF 5 PACKETS PER SECOND \n")
    SERVICE_RATE = 5
    sim_results = s.simulate(service_rate=SERVICE_RATE, queue_size=QUEUE_SIZE, buffer=BUFFER)
    s.graph_plot(sim_results[2], "Queueing delay of each packet (service rate of 5)")
    s.print_sim_data(sim_results=sim_results)

    print("\nSERVICE RATE OF 6 PACKETS PER SECOND \n")
    SERVICE_RATE = 6
    sim_results = s.simulate(service_rate=SERVICE_RATE, queue_size=QUEUE_SIZE, buffer=BUFFER)
    s.graph_plot(sim_results[2], "Queueing delay of each packet (service rate of 6)")
    s.print_sim_data(sim_results=sim_results)

    print("\nSERVICE RATE OF 8 PACKETS PER SECOND \n")
    SERVICE_RATE = 8
    sim_results = s.simulate(service_rate=SERVICE_RATE, queue_size=QUEUE_SIZE, buffer=BUFFER)
    s.graph_plot(sim_results[2], "Queueing delay of each packet (service rate of 8)")
    s.print_sim_data(sim_results=sim_results)

    print()

    
# Execution of the code
if __name__ == "__main__":
    main()