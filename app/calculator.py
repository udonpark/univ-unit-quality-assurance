from datetime import date, datetime
from workalendar.oceania import Australia


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
    # you can choose to initialise variables here, if needed.
    def __init__(self):
        pass

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, configuration, initial_state, final_state, capacity, is_peak, is_holiday):
        if is_peak:
            base_price = 100
        else:
            base_price = 50

        if is_holiday:
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1
        bp = Charger_Configurations().get_base_price(configuration)
        cost = (final_state - initial_state) / 100 * capacity * base_price * bp / 100 * surcharge_factor
        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, configuration, initial_state, final_state, capacity):
        # power=get_power(configuration)
        power = Charger_Configurations.get_power(configuration)
        time = ((final_state - initial_state) / 100 * capacity / power) * 60  # in minutes
        return round(time)

    def is_holiday(self, start_date):
        # use the workalender module and weekends
        # start date is a string
        cal = Australia()
        date_str = datetime.strptime(start_date, "%Y-%m-%d")
        # check if its a holiday or a weekend
        return (not cal.is_working_day(date_str)) or date_str.weekday() > 4

    def is_peak(self, time):
        # assuming that the time is in 24 hr format
        ti = datetime.strptime(time, "%H:%M")
        return ti >= datetime.strptime("06:00", "%H:%M") and ti < datetime.strptime("18:00", "%H:%M")

    # def peak_period(self, start_time):
    #

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







