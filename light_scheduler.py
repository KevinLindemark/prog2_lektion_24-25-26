import schedule
import time
import pigpio

# Global variables
RED_LED_GPIO_PIN = 13
BLUE_LED_GPIO_PIN = 12

class LightScheduler(object):
    """A Python class to turn on/off lights"""
    def __init__(self, LED_GPIO):
        self.LED_GPIO = LED_GPIO
        self.pi = pi = pigpio.pi()
        self.pi.set_PWM_range(LED_GPIO, 100)
        self.timeList = []
        self.dutyList = []
    
    def add_schedule(self, time, duty):
        self.timeList.append(time)
        print(self.timeList)
        self.dutyList.append(duty)
        print(self.dutyList)
    
    def init_schedule(self):
        # set the schedule
        for i in range(len(self.dutyList)):
            print(i)
            # .do second parameter is parameter given to the set_duty function
            schedule.every().day.at(self.timeList[i]).do(self.set_duty, self.dutyList[i])

    def set_duty(self, duty):
        """Sets dutycycle for LED"""
        print(f"Setting duty to : {duty}")
        self.pi.set_PWM_dutycycle(self.LED_GPIO, duty)

if __name__ == "__main__":
    
    # create instance for red LED
    red = LightScheduler(RED_LED_GPIO_PIN)

    # morning red
    red.add_schedule("08:00", 8)
    red.add_schedule("08:10", 16)
    red.add_schedule("08:20", 24)
    red.add_schedule("08:30", 32)
    red.add_schedule("08:40", 40)
    red.add_schedule("08:50", 48)
    red.add_schedule("09:00", 58)
    red.add_schedule("09:10", 48)
    red.add_schedule("09:20", 40)
    red.add_schedule("09:30", 32)
    red.add_schedule("09:40", 24)
    red.add_schedule("09:50", 16)
    red.add_schedule("10:00", 8)

    # evening red
    red.add_schedule("18:10", 16)
    red.add_schedule("18:20", 24)
    red.add_schedule("18:30", 32)
    red.add_schedule("18:40", 40)
    red.add_schedule("18:50", 48)
    red.add_schedule("19:00", 58)
    red.add_schedule("19:10", 48)
    red.add_schedule("19:20", 40)
    red.add_schedule("19:30", 32)
    red.add_schedule("19:40", 24)
    red.add_schedule("19:50", 16)
    red.add_schedule("20:00", 0)

    # initialize red LED schedule
    red.init_schedule()

    # create instance for blue LED
    blue = LightScheduler(BLUE_LED_GPIO_PIN)
    #morning blue
    blue.add_schedule("08:00", 4)
    blue.add_schedule("08:10", 8)
    blue.add_schedule("08:20", 16)
    blue.add_schedule("08:30", 20)
    blue.add_schedule("08:40", 24)
    blue.add_schedule("08:50", 30)
    blue.add_schedule("09:00", 34)
    blue.add_schedule("09:10", 38)
    blue.add_schedule("09:20", 42)
    blue.add_schedule("09:30", 46)
    blue.add_schedule("09:40", 50)
    blue.add_schedule("09:50", 54)
    blue.add_schedule("10:00", 58)
    # evening blue
    blue.add_schedule("18:00", 54)
    blue.add_schedule("18:10", 50)
    blue.add_schedule("18:20", 46)
    blue.add_schedule("18:30", 42)
    blue.add_schedule("18:40", 38)
    blue.add_schedule("18:50", 34)
    blue.add_schedule("19:00", 30)
    blue.add_schedule("19:10", 26)
    blue.add_schedule("19:20", 22)
    blue.add_schedule("19:30", 18)
    blue.add_schedule("19:40", 14)
    blue.add_schedule("19:50", 10)
    blue.add_schedule("20:00", 0)
    
    # initialize blue LED schedule
    blue.init_schedule()
    
    while True:
        schedule.run_pending()
        time.sleep(1)