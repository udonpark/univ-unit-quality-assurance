from datetime import date as date
import datetime
from workalendar.oceania import Australia
import math


class Charger_Configurations:
    configuration = {"1": {"power": 2,
                           "base": 5},
                     "2": {"power": 3.6,
                           "base": 7.5},
                     "3": {"power": 7.2,
                           "base": 10},
                     "4": {"power": 11,
                           "base": 12.5},
                     "5": {"power": 22,
                           "base": 15},
                     "6": {"power": 36,
                           "base": 20},
                     "7": {"power": 90,
                           "base": 30},
                     "8": {"power": 350,
                           "base": 50},
                     }

    def get_power(self, config):
        return self.configuration[str(config)]["power"]

    def get_base_price(self, base_price):
        return self.configuration[str(base_price)]["base"]


class Calculator():
    country = Australia()
    charger = Charger_Configurations()

    def __init__(self, configuration, initial_state, final_state, capacity, postcode, startdate, starttime, power,
                 base_price):
        self.capacity = capacity
        self.postcode = postcode
        self.startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")
        self.starttime = datetime.datetime.strptime(starttime, "%H:%M")
        self.finalstate = final_state
        self.initialstate = initial_state
        self.configuration = configuration
        # calculated variables
        self.base_price = base_price
        self.power = power
        self.total_cal()

    def is_peak(self, time):
        # assuming that the time is in 24 hr format
        ti = time
        return ti >= datetime.datetime.strptime("06:00", "%H:%M") and ti < datetime.datetime.strptime("18:00", "%H:%M")

    def is_holiday(self, start_date):
        # use the workalender module and weekends
        # start date is a string
        cal = Australia()
        date_str = start_date
        # check if its a holiday or a weekend
        return (not cal.is_working_day(date_str)) or date_str.weekday() > 4

    def charge_time(self, final_state, initial_state, capacity, power):
        minutes = math.ceil(
            ((final_state - initial_state) / 100 * capacity / power) * 60)  # convert to minutes from hrs
        # hour=0
        # if minute>59:
        #     hour=minute//60
        #     minute=minute%60
        # charge_time=datetime.time(hours=hour ,minutes=minute)
        return minutes

    def inc_time(self, time):
        ti = time
        ti = datetime.timedelta(minutes=1) + ti
        return ti

    def cal_cost_per_min(self, power, base_price, surcharge, discount):
        cost_per_min = 1 / 60 * power * base_price / 100 * discount * surcharge
        return cost_per_min

    def cal_cost(self, chargetime, base_price, start_time, start_date, power):
        """
        cost= time (in hrs) * power (kwh) * (cost in dollars) c/kwh
        cost/min when time = 1/60
        """
        cost = 0
        surcharge = 1
        discount = 1
        date = start_date  # start_date, "%Y-%m-%d") #initial time
        time = start_time  # atetime.datetime.strptime(start_time, "%H:%M") #initial date
        charge_time = math.ceil(chargetime)
        for minute in range(chargetime):
            if not self.is_peak(time):
                discount = 0.5
            else:
                discount = 1
            if self.is_holiday(date):
                surcharge = 1.1
            else:
                surcharge = 1
            cost += self.cal_cost_per_min(power, base_price, surcharge, discount)
            time = self.inc_time(time)
            date = self.inc_time(date)
        return cost

    # def total_cost(self):
    #     base_price=self.charger.get_base_price(self.configuration)
    #     power=self.charger.get_power(self.configuration)
    #     charge_time=self.charge_time(self.finalstate, self.initialstate, float(power))
    #     self.cost=self.cal_cost(charge_time, base_price, self.starttime, self.startdate)

    def total_cal(self):
        self.duration = self.charge_time(self.finalstate, self.initialstate, self.capacity, self.power)
        self.cost = self.cal_cost(self.duration, self.base_price, self.starttime, self.startdate, self.power)



    def get_duration(self, start_time):
        # total charging time of the car
        pass

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

    # to be acquired through API --
    def get_solar_energy_duration(self, start_time):
        # duration in which car charges while in day light
        pass

    # to be acquired through API --
    def get_day_light_length(self, start_time):
        # sunrise - sunset
        pass

    # to be acquired through API
    def get_solar_insolation(self, solar_insolation):
        pass

    # to be acquired through API
    def get_cloud_cover(self):
        pass

    def calculate_solar_energy(self):
        pass







