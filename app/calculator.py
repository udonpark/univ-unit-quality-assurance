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
        pass

    def is_peak(self):
        pass

    def peak_period(self, start_time):
        pass

    def get_duration(self, start_time):
        pass

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
    def get_solar_energy_duration(self, start_time):
        pass

    # to be acquired through API
    def get_day_light_length(self, postcode,start_date):
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

    # # to be acquired through API
    # def get_solar_insolation(self, solar_insolation): same as sun hour
    #     pass

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


    def calculate_solar_energy(self):
        pass


