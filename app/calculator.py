import requests
import json

class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self):
        pass

    # you may add more parameters if needed, you may modify the formula also.
    def cost_calculation(self, initial_state, final_state, capacity, is_peak, is_holiday):
        if is_peak:
            base_price = 100
        else:
            base_price = 50

        if is_holiday:
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        cost = (final_state - initial_state) / 100 * capacity * base_price / 100 * surcharge_factor
        return cost

    # you may add more parameters if needed, you may also modify the formula.
    def time_calculation(self, initial_state, final_state, capacity, power):
        time = (final_state - initial_state) / 100 * capacity / power
        return time

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_holiday(self, start_date):
        # use the workalender module and weekends
        pass

    def is_peak(self, start_time, end_time):
        # assuming that the time is in 24 hr format
        pass

    # def peak_period(self, start_time):
    #

    def get_duration(self, start_time):
        # total charging time of the car
        pass

    # to be acquired through API
    def get_sun_hour(self, sun_hour):
        pass

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
        # converts minutess to time format. e.g., "150" -> 2:30
        return str(mins // 60) + ":" + str(mins % 60)

    def hours_to_mins(self, hours):
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
