import requests


# Converts temperature values into farenheit
def fahrenheit_conversion(temp):
    return temp * 9 / 5 + 32


# Sets up url string by joining "query" with chosen city
def location():
    query = """https://www.metaweather.com/api/location/search/?query="""

    url = "".join([query, choose_city()])

    # Returns to get_woeid()
    return url


# Handles user input for choosing (major) city. Returns "city" value to
# location()
def choose_city():
    city = input("What city would you like to look up?\n")

    # Replaces spaces so city's string can be added to url
    if " " in city:
        city = city.replace(" ", "%20")
    return city


# Handles request to get the city's woeid after JSON retrieval
def get_woeid():
    r = requests.get(location())
    woeid = str(r.json()[0]["woeid"])

    # Returns to get_url()
    return woeid


# Joins city's woeid to complete location url
def get_url():
    location_url = """https://www.metaweather.com/api/location/"""
    url = "".join([location_url, get_woeid()])

    # Returns to get_weather()
    return url


# Main function for program entry
def get_weather():
    try:
        r = requests.get(get_url())
        weather_data = r.json()

        # Sends weather_data JSON to comb out and print desired values
        forecast(weather_data)

    # Exceptions to handle errors. Retries program if excepted
    except IndexError or requests.exceptions.ConnectionError:
        print("ERROR")
        get_weather()


# Retrieves values from 'consolidate_weather' data and prints output for 6 days
def forecast(weather_data):
    for day in weather_data['consolidated_weather']:
        date = day['applicable_date']
        state = day['weather_state_name']
        temp = str(int(fahrenheit_conversion(day['max_temp']))) + " F"
        print(f"{date}\t {temp}\t {state}")


# Main entry
get_weather()
