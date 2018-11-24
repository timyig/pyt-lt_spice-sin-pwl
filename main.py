
import matplotlib.pyplot as plot
import numpy as np
import math
import datetime
import time
from prettytable import PrettyTable

Pi = math.pi

class SinSignal:

    # Class Attribute
    typ = 'sinus'

    # Initializer / Instance Attributes
    def __init__(self, frequenzy, sample_points):
        self.frequenzy = int(frequenzy)
        self.sample_points = int(sample_points)
        self.sp_degree = np.arange(0, sample_points, 1)
        self.sp_radian = np.arange(0, sample_points, 1)
        self.sp_normalized = np.arange(0, sample_points, 1)
        self.sp_percent = np.arange(0, sample_points, 1)
        self.sp_sin_rad =  np.arange(0, sample_points, 1)
        self.sp_on_time  = np.arange(0, sample_points, 1)
        self.sp_off_time  = np.arange(0, sample_points, 1)
        #the time of one pulse equals to duty cycle 100%
        self.period = 1/self.frequenzy
        self.pulse_time = self.period / self.sample_points
    #Calculates the Sample Points in Rad and Degree
    def calculate_sample_points(self):
        print("Sample Points calculated: ", str(self.sample_points))
        #Rad per Step
        angle_rad = 2*Pi/self.sample_points
        print("Angle between Sample Points in Rad ", "{0:.4f}".format(angle_rad))
        #Degree per Step
        angle_deg = 360/self.sample_points
        print("Angle between Sample Points in Degree ", "{0:.2f}".format(angle_deg))

        print("Calculating Sample Points in Degree")
        self.sp_degree = np.arange(0, int(math.degrees(2*Pi)), angle_deg)
        print("Calculating Sample Points in Rad")
        self.sp_radian = np.arange(0, 2*Pi, angle_rad)

        if self.sp_radian.size != self.sp_degree.size:
            print('You fucked up stupid np.arrange failed')
            exit()

        #Calculate Y Axis Values
        self.sp_sin_rad = np.sin(self.sp_radian)
        print("Calculating Normalized Sample Points")
        #Don't want to have negative values therefore lift the sinwave by 1
        self.sp_normalized = 1 + self.sp_sin_rad
        print("Calculating Sample Points in %")
        self.sp_percent = self.sp_normalized / 2
        print("Calculating On Time for Pulses")
        on_time  = self.pulse_time * self.sp_percent
        print("Calculating Off Time for Pulses")
        off_time = self.pulse_time - on_time 

    def plot_sample_points(self):

        print("Ploting Table: ", str(self.sample_points))

        #Doing some logic here to have prettier prints
        time_unit_multiplier = 1
        period_unit_multiplier = 1
        TimeUnitPeriod = "s"
        TimeUnitPulse  = "s"

        if self.frequenzy <= 1000:
                #Frequenzy Below 1KHz
                time_unit_multiplier = 1000
                period_unit_multiplier = 1000
                TimeUnitPeriod = "ms"
                TimeUnitPulse  = "us"

        index = 0

        x = PrettyTable()
        x.field_names = ["Sample Points", str(self.sample_points)]
        x.add_row(["Period in "+ TimeUnitPeriod, " {0:.2f}" .format(self.period*period_unit_multiplier )])
        x.add_row(["Pulse time in "+ TimeUnitPeriod, " {0:.2f}" .format(self.pulse_time*time_unit_multiplier )])
        print(x)

        OnTimeHeader = "On Time in " + TimeUnitPulse
        OffTimeHeader = "Off Time in " + TimeUnitPulse
        index = 0
        y = PrettyTable()
        y.field_names = ["Degree", "Radian", "sine(Radian)", "Normalized", "Percent", OnTimeHeader, OffTimeHeader]

        for x in np.nditer(self.sp_degree):
            y.add_row(["{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_radian[index]),
            "{0:.2f}".format(self.sp_normalized[index]),
            "{0:.1f}".format((self.sp_percent[index])*100),
            "{0:.8f}".format(self.sp_on_time[index]* time_unit_multiplier),
            "{0:.8f}".format(self.sp_off_time[index]* time_unit_multiplier)])

            index += 1

        print('Calculated at - ' + datetime.datetime.now().strftime("%d-%m-%Y  %H:%M"))
        print(y)

    def plot_OnTime(self):

        print("Plot OnTime")

        sample_time = (self.sp_radian/2*Pi)*self.period

        #Doing some logic here to have prettier prints
        time_unit_multiplier = 1
        period_unit_multiplier = 1
        TimeUnitPeriod = "s"
        TimeUnitPulse  = "s"

        if self.frequenzy <= 1000:
                #Frequenzy Below 1KHz
                time_unit_multiplier = 1000
                period_unit_multiplier = 1000
                TimeUnitPeriod = "ms"
                TimeUnitPulse  = "us"

        high_on  = sample_time -(self.sp_on_time/2)
        high_off = sample_time +(self.sp_on_time/2)

        index = 0

        x = PrettyTable()
        x.field_names = ["Sample Points", str(self.sample_points)]
        x.add_row(["Period in "+ TimeUnitPeriod, " {0:.2f}" .format(self.period*period_unit_multiplier )])
        x.add_row(["Pulse time in "+ TimeUnitPeriod, " {0:.2f}" .format(self.pulse_time*time_unit_multiplier )])
        x.add_row(["Frequenzy ", str(self.frequenzy)])

        print(x)

        OnTimeHeader = "On Time in " + TimeUnitPulse
        OffTimeHeader = "Off Time in " + TimeUnitPulse
        index = 0
        y = PrettyTable()
        y.field_names = ["Degree", "Radian", "sine(Radian)", "Normalized", "Percent", 'Sample Time', 'High Time On', 'High Time Off', OnTimeHeader, OffTimeHeader]

        for x in np.nditer(self.sp_degree):
            y.add_row(["{0:.2f}".format(self.sp_degree[index]),
            "{0:.2f}".format(self.sp_radian[index]),
            "{0:.2f}".format(self.sp_sin_rad[index]),
            "{0:.2f}".format(self.sp_normalized[index]),
            "{0:.1f}".format((self.sp_percent[index])*100),
            "{0:.2f}".format((sample_time[index])*1000),
            "{0:.2f}".format((high_on[index])*1000),
            "{0:.2f}".format((high_off[index])*1000),
            "{0:.8f}".format(self.sp_on_time[index]* time_unit_multiplier),
            "{0:.8f}".format(self.sp_off_time[index]* time_unit_multiplier)])

            index += 1

        print('Calculated at - ' + datetime.datetime.now().strftime("%d-%m-%Y  %H:%M"))
        print(y)

        FileName = 'Frequenzy_'+ str(self.frequenzy) + 'Hz'+'.pwl'
        print(FileName)
        with open(FileName,'w') as pwl:
            pwl.write(str(y))

        t = (on_time*1000)
        s = degree
        plot.bar(s, t)

        plot.xlabel('Degree')
        plot.ylabel('OnTime')
        plot.title('OnTime')
        plot.grid(True)
        plot.show()

def main():
    print ("Starting main()")
    signal = SinSignal(100,128)
    signal.calculate_sample_points()
    signal.plot_sample_points()

main()
