import os
import requests
from requests import HTTPError
from Flight import Flight
import sqlite3
from datetime import datetime

search_timestamp = None
headers = {
    "accept": "application/json",
    "apikey": os.environ.get("apikey"),
}


def create_search_results_table():
    global search_timestamp
    # Create a table name
    search_timestamp = f'search_{datetime.now().strftime("%d/%m/%y_%H:%M:%S")}'
    # Connect to database and create table to store results
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"create table '{search_timestamp}' ("
                   "flying_from text,"
                   "flying_to text,"
                   "departure_date text,"
                   "departure_time text,"
                   "nights_at_destination text,"
                   "price text,"
                   "booking_link text"
                   ")")
    connection.commit()
    connection.close()


def get_departure_code(departure):
    departure_parameters = {
        "term": departure
    }

    departure_response = requests.get(url="https://api.tequila.kiwi.com/locations/query", headers=headers,
                                      params=departure_parameters)
    departure_response.raise_for_status()
    departure_data = departure_response.json()
    return departure_data['locations'][0]['code']


def get_destination_codes(destinations):
    destinations_dict = {}
    for destination in destinations:
        destination_parameters = {
            "term": destination
        }

        destination_response = requests.get(url="https://api.tequila.kiwi.com/locations/query", headers=headers,
                                            params=destination_parameters)
        destination_response.raise_for_status()
        destination_data = destination_response.json()
        destinations_dict.update({destination_data["locations"][0]["code"]: destination})
        print(f"{destination_data['locations'][0]['code']}")

    print(f"Updated IATA codes.\nTotal entries: {len(destinations_dict)}")
    return destinations_dict


def get_all_search_results(search_parameters):
    global headers
    search_results = []
    try:
        print(f"Fetching data for {search_parameters['fly_to']}...")
        search_response = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=headers,
                                       params=search_parameters)
        search_response.raise_for_status()
        search_data = search_response.json()

        print(f"Data for {search_parameters['fly_to']} retrieved.")
        for flight in search_data["data"]:
            search_results.append(Flight(flying_from=flight["flyFrom"],
                                         city_from=flight["cityFrom"],
                                         country_from=flight["countryFrom"],
                                         flying_to=flight["flyTo"],
                                         city_to=flight["cityTo"],
                                         country_to=flight["countryTo"],
                                         departure=flight["local_departure"],
                                         nights=flight["nightsInDest"],
                                         price=flight["price"],
                                         link=flight["deep_link"]
                                         ))
        print(f"{len(search_results)} flights to {search_parameters['fly_to']} found.")
        return search_results

    except HTTPError:
        print("Servers are busy, please try again in a few seconds! No data has been fetched.")
        return search_results


def get_cheapest_flights(search_results, departure, destination):
    cheapest_flights = []
    try:
        # Find the cheapest flight among search results
        cheapest_flight = search_results[0]
        print("Filtering cheapest flights.")
        for flight in search_results:
            if flight.price < cheapest_flight.price:
                cheapest_flight = flight
            else:
                pass

        # Add all cheap flights to the list
        for flight in search_results:
            if flight.price == cheapest_flight.price:
                cheapest_flights.append(flight)
            else:
                pass

        # Return list sorted by departure dates
        print(f"Processed cheapest flights to {destination}, {len(cheapest_flights)} flights added.\n")
        cheapest_flights.sort()
        return cheapest_flights

    except IndexError:
        print(f"No direct flights found for {destination} from {departure}.\n")
        return cheapest_flights


def add_flights_to_table(cheapest_flights):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    for flight in cheapest_flights:
        cursor.execute(f"insert into '{search_timestamp}' values (?,?,?,?,?,?,?)",
                       (flight.formatted_from, flight.formatted_to, flight.departure_date,
                        flight.departure_time, flight.nights_at_destination, flight.price, flight.deep_link))
    connection.commit()
    connection.close()


def search(departure, destinations, from_date, to_date, max_stopovers, min_nights, max_nights):
    global search_timestamp
    global headers

    create_search_results_table()

    departure_dictionary = get_departure_code(departure)
    destinations_dictionary = get_destination_codes(destinations.split(", "))

    for key in destinations_dictionary.keys():

        search_parameters = {
            "fly_from": departure_dictionary,
            "fly_to": key,
            "date_from": from_date,
            "date_to": to_date,
            "curr": "EUR",
            "max_stopovers": max_stopovers,
            "nights_in_dst_from": min_nights,
            "nights_in_dst_to": max_nights,
        }

        search_results = get_all_search_results(search_parameters)
        cheapest_flights = get_cheapest_flights(search_results, search_parameters['fly_from'], search_parameters['fly_to'])
        add_flights_to_table(cheapest_flights)
