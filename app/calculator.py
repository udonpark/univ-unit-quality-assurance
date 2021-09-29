import requests
import json



from datetime import date as date
import datetime
from workalendar.oceania import Australia
import math





class Calculator():
    country = Australia()

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



    # to be acquired through API
    def get_sun_hour(self, postcode, start_date):
        location_id = ""
        start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api

        #for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode='+str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get('http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=' + start_date1)
        response_data1 = response1.json()
        return response_data1['sunHours'] #sunHours aka solar insolation

    # to be acquired through API
    def get_day_light_length(self, postcode, start_date, start_time):
        location_id = ""
        start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api

        #for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode='+str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get('http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=+' + start_date1)
        response_data1 = response1.json()

        sunrise = response_data1['sunrise']
        sunrise = sunrise.split(":")
        sunrisehours = sunrise[0]
        sunrisemins = sunrise[1]

        sunset = response_data1['sunset']
        sunset = sunset.split(":")
        sunsethours = sunset[0]
        sunsetmins = sunset[1]

        hours_difference = sunsethours - sunrisehours
        mins_difference = sunsetmins - sunrisemins

        return hours_difference + (mins_difference/60)

    def add_time(self, time1, time2):
        # add two times in string format. e.g., "10:30" + "4:40" -> "15:10"
        time1 = time1.split(":")
        time2 = time2.split(":")
        sum_mins = int(time1[0]) * 60 + int(time2[0]) * 60 + int(time1[1]) + int(time2[1])
        sum_hours = str(sum_mins // 60) + ":" + str(sum_mins % 60)
        return sum_hours

    def minus_time(self, start_time, end_time):
        # minus two times in string format. e.g., "10:30" - "4:40" -> "5:50"
        start_time = start_time.split(":")
        end_time = end_time.split(":")
        difference_mins = (int(end_time[0]) * 60 + int(end_time[1])) - (int(start_time[0]) * 60 + int(start_time[1]))
        difference_hours = str(difference_mins // 60) + ":" + str(difference_mins % 60)
        return difference_hours

    def mins_to_hours(self, mins):
        # converts minutes to time format. e.g., "150" -> 2:30
        return str(mins // 60) + ":" + str(mins % 60)

    def hours_to_mins(self, hours):
        # converts hours to minutes. e.g., "2:30" -> 150
        hours = hours.split(":")
        return int(hours[0]) * 60 + int(hours[1])

    # to be acquired through API --
    def get_solar_energy_duration(self, postcode, start_date, start_time, charging_length):
        # duration in which car charges while in day light
        location_id = ""
        start_date1 = str(start_date)[::-1]  # start date in reverse form as start date input is in reverse in the api

        # for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode=' + str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get(
            'http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=+' + start_date1)
        response_data1 = response1.json()

        # obtain sunrise and sunset times, and also end time of the charging process
        end_time = self.add_time(start_time, self.minus_time(charging_length))
        sunrise = response_data1['sunrise']
        sunset = response_data1['sunset']

        # make sure to calculate charging time during daylight hours
        if self.hours_to_mins(sunrise) > self.hours_to_mins(start_time):
            start_time = sunrise

        if self.hours_to_mins(sunset) < self.hours_to_mins(end_time):
            end_time = sunset

        # calculate and return duration time in minutes
        duration_hours = self.minus_time(start_time, end_time)
        return self.hours_to_mins(duration_hours)

    # to be acquired through API
    def get_cloud_cover(self, postcode, start_date, start_time):

        location_id = ""
        start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api

        #for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode='+str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get('http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=+' + start_date1)
        response_data1 = response1.json()
        hour = response_data1['hourlyWeatherHistory']

        start_time1 = start_time.split(":")
        #here we get the cloud cover for the specific time
        for b in hour:
            if b["hour"] == start_time1[0]:
                return b["cloudCoverPct"] #the cloud cover


    def calculate_solar_energy(self, start_date):
        pass



