from time import sleep
import pigpio
pi = pigpio.pi()
GPIO_RED_LED = 13
GPIO_BLUE_LED = 12

pi.set_PWM_range(GPIO_RED_LED, 100)
pi.set_PWM_range(GPIO_BLUE_LED, 100)

pi.set_PWM_frequency(GPIO_RED_LED, 100000)
pi.set_PWM_frequency(GPIO_BLUE_LED, 100000)

pi.set_PWM_dutycycle(GPIO_BLUE_LED, 10)
sleep(2)
pi.set_PWM_dutycycle(GPIO_BLUE_LED, 0)

pi.set_PWM_dutycycle(GPIO_RED_LED, 10)
sleep(2)
pi.set_PWM_dutycycle(GPIO_RED_LED, 0)

