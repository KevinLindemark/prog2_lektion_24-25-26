import schedule
import time
import pigpio
import adc_moist
<<<<<<< HEAD
import insert_soilmoisture_data
=======
>>>>>>> 5794b533bf8062986eabb2f9426d8d83c0e278d4
# Global variables
PUMP_GPIO_PIN = 17

class PumpScheduler:
    """A Python class to turn control waterpump based on soilmoisture and time of the day"""
    def __init__(self, PUMP_GPIO_PIN):
        self.PUMP_GPIO_PIN = PUMP_GPIO_PIN
        self.pi = pigpio.pi()
        self.timeList = []
    
    def add_schedule(self, time):
        self.timeList.append(time)
        print(self.timeList)

    def init_schedule(self):
        # set the schedule
        for i in range(len(self.timeList)):
            print(i)
            # .do second parameter is parameter given to the set_duty function
            schedule.every().day.at(self.timeList[i]).do(self.change_pump_state)

    def change_pump_state(self):
<<<<<<< HEAD
        """Sets state for Pump 1 for ON 0 for OFF"""
        soil_moisture = adc_moist.get_soilmoisture_percentage()
        print(f"Checking soilmosture and it is {soil_moisture}% moist")
        if soil_moisture:
            insert_soilmoisture_data.insert_moisture_data(soil_moisture)
        else:
            print("no data to insert in database")
    
        if soil_moisture < 30:
=======
        """Sets state for Pump - 1 for ON 0 for OFF"""
        soil_moisture = adc_moist.get_soilmoisture_percentage()
        print(f"Checking soilmosture and it is {soil_moisture}% moist")
        if soil_moisture < 10:
>>>>>>> 5794b533bf8062986eabb2f9426d8d83c0e278d4
            try:
                print("soil is dry starting pump for 10 seconds")
                self.pi.write(self.PUMP_GPIO_PIN, 1)
                # the pump gives aproximately 200 mililiters of water per 10 seconds
                time.sleep(10)
                self.pi.write(self.PUMP_GPIO_PIN, 0)
            except:
                print("Something went wrong, stopping pump")
                self.pi.write(self.PUMP_GPIO_PIN, 0)
        else:
            print("The soil did not need watering")

if __name__ == "__main__":
    
    # create instance for Pump Scheduler 
    pump = PumpScheduler(PUMP_GPIO_PIN)
    # morning watering
    pump.add_schedule("07:00")
    # initialize red LED schedule
    pump.init_schedule()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
