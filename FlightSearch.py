import os
import requests
from requests import HTTPError
from FlightData import FlightData


def search(departure, destinations, fromDate, toDate, maxStopovers, minNights, maxNights):
    file = open("data/Cheapest Flights.txt", "w")
    file.close()

    headers = {
        "accept": "application/json",
        "apikey": os.environ.get("apikey"),
    }
    destinationsDict = {}
    destinationList = destinations.split(", ")
    searchResults = []
    cheapestFlights = []

    departureParameters = {
        "term": departure
    }

    departureResponse = requests.get(url="https://api.tequila.kiwi.com/locations/query", headers=headers,
                                     params=departureParameters)
    departureResponse.raise_for_status()
    departureData = departureResponse.json()
    departureCode = departureData['locations'][0]['code']

    for destination in destinationList:
        destinationParameters = {
            "term": destination
        }

        destinationResponse = requests.get(url="https://api.tequila.kiwi.com/locations/query", headers=headers,
                                           params=destinationParameters)
        destinationResponse.raise_for_status()
        destinationData = destinationResponse.json()
        destinationsDict.update({destinationData["locations"][0]["code"]: destination})
        print(f"{destinationData['locations'][0]['code']}")

    print(f"Updated IATA codes.\nTotal entries: {len(destinationsDict)}")

    for key in destinationsDict.keys():

        searchResults.clear()
        cheapestFlights.clear()

        searchParameters = {
            "fly_from": departureCode,
            "fly_to": key,
            "date_from": fromDate,
            "date_to": toDate,
            "curr": "EUR",
            "max_stopovers": maxStopovers,
            "nights_in_dst_from": minNights,
            "nights_in_dst_to": maxNights,
        }

        try:
            print(f"Connecting to server, fetching data for {searchParameters['fly_to']}...")
            searchResponse = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=headers,
                                          params=searchParameters)
            searchResponse.raise_for_status()
            searchData = searchResponse.json()

            print(f"Data for {searchParameters['fly_to']} retrieved.")
            for flight in searchData["data"]:
                searchResults.append(FlightData(fly_from=flight["flyFrom"],
                                                city_from=flight["cityFrom"],
                                                country_from=flight["countryFrom"],
                                                fly_to=flight["flyTo"],
                                                city_to=flight["cityTo"],
                                                country_to=flight["countryTo"],
                                                departure=flight["local_departure"],
                                                nights=flight["nightsInDest"],
                                                price=flight["price"],
                                                link=flight["deep_link"]
                                                ))

        except HTTPError:
            print("Servers are busy, please try again in a few seconds!")

        try:
            # Find the cheapest flight among search results
            cheapest_flight = searchResults[0]
            for flight in searchResults:
                if flight.price < cheapest_flight.price:
                    cheapest_flight = flight
                else:
                    pass

            # Add all cheap flights to the list
            for flight in searchResults:
                if flight.price == cheapest_flight.price:
                    cheapestFlights.append(flight)
                else:
                    pass

            # Sort the cheapest flights by date and save them to a file
            cheapestFlights.sort()
            for flight in cheapestFlights:
                with open("data/Cheapest Flights.txt", "a") as file:
                    file.write(str(flight))

        except IndexError:
            print(
                f"No direct flights found for {searchParameters['fly_to']} from {searchParameters['fly_from']}\n")

        else:
            print(f"{len(searchResults)} flights to {searchParameters['fly_to']} found.")
            print(
                f"Processed cheapest flights to {searchParameters['fly_to']}, {len(cheapestFlights)} flights added.\n")

    os.startfile(os.path.abspath("data/Cheapest Flights.txt"))
