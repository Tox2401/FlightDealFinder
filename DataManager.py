import requests
import pandas
from datetime import datetime, timedelta
from FlightSearch import FlightSearch
from NotificationManager import NotificationManager
import os


while True:
    registrationPrompt = input("Do you want to register and receive updates for latest cheap flights? (Y/N): ")

    if registrationPrompt.upper() == "Y":
        NotificationManager.addUser()

    elif registrationPrompt.upper() == "N":
        break

    else:
        print("Invalid input, try again (Enter Y/N) ")

    while True:
        anotherUserPrompt = input("Do you want to add another user? (Y/N): ")
        if anotherUserPrompt.upper() == "Y":
            NotificationManager.addUser()
        elif anotherUserPrompt.upper() == "N":
            break
        else:
            print("Invalid input, try again (Enter Y/N) ")

    break

headers = {
    "accept": "application/json",
    "apikey": os.environ.get("apikey"),
}

flightDeals = pandas.read_csv("data/Flight Deals.csv")
iata_codes = []

for index, row in flightDeals.iterrows():

    parameters = {
        "term": row["City"]
    }

    response = requests.get(url="https://api.tequila.kiwi.com/locations/query", headers=headers, params=parameters)
    response.raise_for_status()
    data = response.json()
    iata_codes.append(data["locations"][0]["code"])

flightDeals["IATA Code"] = iata_codes
flightDeals.to_csv("data/Flight Deals.csv", index=False)
print(f"Updated IATA codes:\n{iata_codes}\nTotal entries: {len(iata_codes)}")

dateTomorrow = (datetime.now() + timedelta(1)).strftime('%d/%m/%Y')
dateInSixMonths = (datetime.now() + timedelta(180)).strftime('%d/%m/%Y')

for index, row in flightDeals.iterrows():
    searchParameters = {
        "fly_from": "ZAG",
        "fly_to": row["IATA Code"],
        "date_from": dateTomorrow,
        "date_to": dateInSixMonths,
        "curr": "EUR",
        "max_stopovers": 0,
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 14
    }

    fs = FlightSearch(flightDeals, searchParameters)
    fs.search()
