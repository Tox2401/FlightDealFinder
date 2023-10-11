import os
import requests
from requests import HTTPError
from FlightData import FlightData


class FlightSearch:

    def __init__(self, flightDeals, searchParameters):
        self.flightDeals = flightDeals
        self.searchParameters = searchParameters
        self.searchResults = []
        self.cheapestFlights = []

    def search(self):

        headers = {
            "accept": "application/json",
            "apikey": os.environ.get("apikey"),
        }

        self.searchResults.clear()
        self.cheapestFlights.clear()
        try:
            print(f"Connecting to server, fetching data for {self.searchParameters['fly_to']}...")
            searchResponse = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=headers,
                                          params=self.searchParameters)
            searchResponse.raise_for_status()
            searchData = searchResponse.json()

            print(f"Data for {self.searchParameters['fly_to']} retrieved.")
            for flight in searchData["data"]:
                self.searchResults.append(FlightData(fly_from=flight["flyFrom"],
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
            FlightSearch.searchCheapest(self)

        except IndexError:
            print(f"No direct flights found for {self.searchParameters['fly_to']} from {self.searchParameters['fly_from']}\n")

        else:
            print(f"{len(self.searchResults)} flights to {self.searchParameters['fly_to']} found.")
            print(f"Processed cheapest flights to {self.searchParameters['fly_to']}, {len(self.cheapestFlights)} flights added.\n")

    def searchCheapest(self):
        # Find the cheapest flight among search results
        cheapest_flight = self.searchResults[0]
        for flight in self.searchResults:
            if flight.price < cheapest_flight.price:
                cheapest_flight = flight
            else:
                pass

        # Add all cheap flights to the list
        for flight in self.searchResults:
            if flight.price == cheapest_flight.price:
                self.cheapestFlights.append(flight)
            else:
                pass

        # Sort the cheapest flights by date and save them to a file
        self.cheapestFlights.sort()
        for flight in self.cheapestFlights:
            with open("data/Cheapest Flights.txt", "a") as file:
                file.write(str(flight))
