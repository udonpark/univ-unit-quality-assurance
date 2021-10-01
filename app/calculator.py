import requests
import json

from datetime import date as date
import datetime
from requests.models import Response
from workalendar.oceania import Australia
import math


class Calculator():
    country = Australia()
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

    def __init__(self):
        pass

    def get_power(self, config):
        return self.configuration[str(config)]["power"]

    def get_base_price(self, config):
        return self.configuration[str(config)]["base"]

    def is_peak(self, time):
        # assuming that the time is in 24 hr format
        ti=time
        if not isinstance(ti, datetime.datetime):
            ti = datetime.datetime.strptime(time, "%H:%M")
        return ti >= datetime.datetime.strptime("06:00", "%H:%M") and ti <= datetime.datetime.strptime("18:00", "%H:%M")

    def is_holiday(self, start_date):
        # use the workalender module and weekends
        # start date is a string
        cal = Australia()
        date_str=start_date
        if not isinstance(date_str, datetime.datetime):
            date_str= datetime.datetime.strptime(start_date, "%Y-%m-%d")
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
        date = datetime.datetime.strptime(start_date, "%Y-%m-%d")   # start_date, "%Y-%m-%d") #initial time
        time = datetime.datetime.strptime(start_time, "%H:%M")   # datetime.datetime.strptime(start_time, "%H:%M") #initial date
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

    # def total_cal(self):
    #     self.duration = self.charge_time(self.finalstate, self.initialstate, self.capacity, self.power)
    #     self.cost = self.cal_cost(self.duration, self.base_price, self.starttime, self.startdate, self.power)



    # to be acquired through API
    def get_sun_hour(self, postcode, start_date):
        location_id = ""
        # start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api
        start_date = start_date.split("-")
        start_date1 = start_date[2] + "-" + start_date[1] + "-" + start_date[0]
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
    def get_day_light_length(self, postcode, start_date):
        location_id = ""
        # start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api
        start_date = start_date.split("-")
        start_date1 = start_date[2] + "-" + start_date[1] + "-" + start_date[0]

        #for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode='+str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get('http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=' + start_date1)
        response_data1 = response1.json()

        sunrise = response_data1['sunrise']
        sunrise = sunrise.split(":")
        sunrisehours = sunrise[0]
        sunrisemins = sunrise[1]

        sunset = response_data1['sunset']
        sunset = sunset.split(":")
        sunsethours = sunset[0]
        sunsetmins = sunset[1]

        hours_difference = int(sunsethours) - int(sunrisehours)
        mins_difference = int(sunsetmins) - int(sunrisemins)

        return hours_difference + (mins_difference/60)

    def add_time(self, time1, time2): 
        # add two times in string format. e.g., "10:30" + "4:40" -> "15:10"
        time1 = time1.split(":")
        time2 = time2.split(":")
        sum_mins = int(time1[0]) * 60 + int(time2[0]) * 60 + int(time1[1]) + int(time2[1])
        sum_hours = str(sum_mins // 60) + ":" + str(sum_mins % 60)
        if sum_mins%60<10:
            sum_hours+="0"
        return sum_hours

    def minus_time(self, start_time, end_time):
        # minus two times in string format. e.g., "10:30" - "4:40" -> "5:50"
        start_time = start_time.split(":")
        end_time = end_time.split(":")
        difference_mins = (int(end_time[0]) * 60 + int(end_time[1])) - (int(start_time[0]) * 60 + int(start_time[1]))
        difference_hours = str(difference_mins // 60) + ":" + str(difference_mins % 60)
        return difference_hours

    def m_to_h(self, mins):
        # converts minutes to hours time format. e.g., "150" -> 2:30
        out= str(mins // 60) + ":" + str(mins % 60) 
        if mins%60<10:
            out+="0"
        return out

    def h_to_m(self, hours):
        # converts hours to minutes. e.g., "2:30" -> 150
        hours = hours.split(":")
        return int(hours[0]) * 60 + int(hours[1])

    # to be acquired through API --
    def get_solar_energy_duration(self, postcode, start_date, start_time, charging_length):
        # duration in which car charges while in day light
        location_id = ""
        # start_date1 = str(start_date)[::-1]  # start date in reverse form as start date input is in reverse in the api
        start_date = start_date.split("-")
        start_date1 = start_date[2] + "-" + start_date[1] + "-" + start_date[0]

        # for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode=' + str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get(
            'http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=' + start_date1)
        response_data1 = response1.json()

        # obtain sunrise and sunset times, and also end time of the charging process
        end_time = self.add_time(start_time, self.m_to_h(charging_length))
        sunrise = response_data1['sunrise'] 
        if len(sunrise) == 8:
            sunrise = sunrise[:-3]
        sunset = response_data1['sunset']
        if len(sunset) == 8:
            sunset = sunset[:-3]

        # print("start time="+start_time)
        # print("end time="+ end_time)
        # make sure to calculate charging time during daylight hours
        if self.h_to_m(sunrise) > self.h_to_m(start_time):
            start_time = sunrise

        if self.h_to_m(sunset) < self.h_to_m(end_time):
            end_time = sunset
        # print(end_time)
        #end_time=end_time[:-3]
        # calculate and return duration time in minutes
        duration_hours = self.minus_time(start_time, end_time)
        return self.h_to_m(duration_hours), start_time, end_time

    # to be acquired through API
    def get_cloud_cover(self, postcode, start_date, start_time):

        location_id = ""
        # start_date1 = str(start_date)[::-1] #start date in reverse form as start date input is in reverse in the api
        start_date = start_date.split("-")
        start_date1 = start_date[2] + "-" + start_date[1] + "-" + start_date[0]

        #for the location id
        response = requests.get('http://118.138.246.158/api/v1/location?postcode='+str(postcode))
        response_data = response.json()

        for a in response_data:
            location_id += a['id']

        # for sun hours duration
        response1 = requests.get('http://118.138.246.158/api/v1/weather?location=' + location_id + '&date=' + start_date1)
        response_data1 = response1.json()
        hour = response_data1['hourlyWeatherHistory']

        start_time1 = start_time.split(":")
        #here we get the cloud cover for the specific time
        for b in hour:
            if b["hour"] == start_time1[0]:
                return b["cloudCoverPct"] #the cloud cover

    def solar_energy_aux(self, start_date, start_time, post_code, final_state, initial_state, capacity, power):
        si = self.get_sun_hour(post_code, start_date)
        dl = self.get_day_light_length(post_code, start_date)
        charging_length = self.charge_time(final_state, initial_state, capacity, power)

        du = self.get_solar_energy_duration(post_code, start_date, start_time, charging_length)[0]
        st = self.get_solar_energy_duration(post_code, start_date, start_time, charging_length)[1]
        et = self.get_solar_energy_duration(post_code, start_date, start_time, charging_length)[2]

        hours_list = []
        time_iterator = st
        while self.h_to_m(time_iterator) < self.h_to_m(et):
            if self.h_to_m(time_iterator) // 60 == (self.h_to_m(et) // 60):
                hours_list.append(time_iterator)
                hours_list.append(et)
                time_iterator = et
            else:
                if self.h_to_m(time_iterator) % 60 != 0:
                    hours_list.append(time_iterator)  # eg, 8:40
                    time_iterator = self.add_time(time_iterator, self.m_to_h(60 - (self.h_to_m(time_iterator) % 60)))
                else:
                    hours_list.append(time_iterator)
                    time_iterator = self.add_time(time_iterator, "1:00")
                    
                    # et is 13:30
                    # 11, 12, 13, 13:30

        generation_list = []
        for i in range(len(hours_list) - 1):
            duration = self.h_to_m(self.minus_time(hours_list[i], hours_list[i + 1]))
            cc = self.get_cloud_cover(post_code, start_date, hours_list[i])
            if cc is None:
                generation_list.append(si * 1 / dl * (1 / 100) * 50 * 0.20 * duration / 60)
                continue
            generation_list.append(si * 1 / dl * (1 - cc / 100) * 50 * 0.20 * duration / 60)

        """
        7:20 -13:30
        generation_list = [34, 45, 65, 34, 45, 56, 32]
        hours_list = [7:20, 8:00, 9:00, 10:00, 11:00, 12:00, 13:00, 13:20]
        """
        return generation_list, hours_list, et
    #ko
    def calculate_solar_energy(self, inputdate, start_time, post_code, final_state, initial_state, capacity, power):
        ref = datetime.date.today().year
        reference_date = ""
        start_date = inputdate.split("-")
        inputdate = start_date[2] + "-" + start_date[1] + "-" + start_date[0]

        inputdate = datetime.datetime.strptime(inputdate, "%Y-%m-%d")
        if inputdate.year > ref:
            dates = str(inputdate).split(" ")[0].split("-", 1)
            reference_date = str(ref) + "-" + dates[1]
            month = dates[1].split("-")[0]
            day = dates[1].split("-")[-1]
            try:
                datetime.datetime.strptime(reference_date, "%Y-%m-%d")
            except ValueError:
                reference_date = str(ref) + '-' + month + '-' + str((int(day) - 1))
        else:
            reference_date = str(str(inputdate).split(" ")[0])
        dates = str(inputdate).split(" ")[0].split("-", 1)

        # new_date = datetime.datetime.strptime(reference_date, "%Y-%m-%d")
        temp_date = reference_date.split("-")
        reference_date = temp_date[2] + "-" + temp_date[1] + "-" + temp_date[0]

        list1 = self.solar_energy_aux(reference_date, start_time, post_code, final_state, initial_state, capacity, power)[0]
        hour_list = self.solar_energy_aux(reference_date, start_time, post_code, final_state, initial_state, capacity, power)[1]
        # reference_date = str(int(ref - 1)) + str(dates[0])
        reference_date = temp_date[2] + "-" + temp_date[1] + "-" + str(int(temp_date[0])-1)
        list2 = self.solar_energy_aux(reference_date, start_time, post_code, final_state, initial_state, capacity, power)[0]
        # reference_date = str(int(temp_date[2])) + "-" + temp_date[1] + "-" + temp_date[0]
        reference_date = temp_date[2] + "-" + temp_date[1] + "-" + str(int(temp_date[0]) - 2)
        list3 = self.solar_energy_aux(reference_date, start_time, post_code, final_state, initial_state, capacity, power)[0]

        mean_list = []
        for i in range(len(list1)):
            mean_list.append((float(list1[i]) + float(list2[i]) + float(list3[i])) / 3)
        return mean_list, hour_list

    """
    9:30 - 13:20
    [9:30, 10:00, 11:00, 12:00, 13:00, 13:20] <- hour_list
    [energy1, energy2, energy3, energy4, energy5] <- mean_list
    """
    def calculate_charging_cost(self, start_date, start_time, post_code, final_state, initial_state, capacity, power, config):
        mean_list = self.calculate_solar_energy(start_date, start_time, post_code, final_state, initial_state, capacity, power)[0]
        hour_list = self.calculate_solar_energy(start_date, start_time, post_code, final_state, initial_state, capacity, power)[1]
        cost = 0
        total_energy = 0
        for i in range(mean_list):
            # self, chargetime, base_price, start_time, start_date, power
            solar = mean_list[i]
            net = self.get_power(config) - solar
            cost += self.cal_cost(self.h_to_m(self.minus_time(hour_list[i], hour_list[i + 1])), self.get_base_price(config), hour_list[i], start_date, net)
            total_energy += mean_list[i]

        charging_time = self.charge_time(final_state, initial_state, capacity, power)
        et = self.add_time(start_time, self.m_to_h(charging_time))

        # if charging takes place outside sunrise hours, we have to take it into account its cost as well
        if (self.h_to_m(start_time)) < self.h_to_m(hour_list[0]):
            cost += self.cal_cost(self.h_to_m(self.minus_time(start_time, self.h_to_m(hour_list[0]))), self.get_base_price(config), start_time, start_date, power)
        if (self.h_to_m(et)) > self.h_to_m(hour_list[-1]):
            cost += self.cal_cost(self.h_to_m(self.minus_time(self.h_to_m(hour_list[-1]), et)), self.get_base_price(config), start_time, start_date, power)

        # return total_energy if curious
        return cost

    @property
    def get(self):
        try:
            r = requests.get('http://118.138.246.158/api/v1/location=ab9f494f-f8a0-4c24-bd2e-2497b99f2258?postcode=3800', timeout=1)

            if r.ok:
                return r
            else:
                return None

        except requests.exceptions.Timeout:
            return "Bad Response"

