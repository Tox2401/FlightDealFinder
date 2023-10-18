class FlightData:

    def __init__(self, fly_from, city_from, country_from, fly_to, city_to, country_to, departure, nights, price, link):
        format_date = departure.split("T")
        self.fly_from = fly_from
        self.city_from = city_from
        self.country_from = country_from
        self.formatted_from = f"{city_from} ({fly_from}), {country_from['name']}"
        self.fly_to = fly_to
        self.city_to = city_to
        self.country_to = country_to
        self.formatted_to = f"{city_to} ({fly_to}), {country_to['name']}"
        self.departure_date = format_date[0]
        self.departure_time = format_date[1]
        self.nights_in_dest = nights
        self.price = price
        self.deep_link = link

    def __str__(self):
        return f"***************************************************************************************************\n"\
               f"Flying from: {self.city_from} ({self.fly_from}), {self.country_from['name']}\n" \
               f"Flying to: {self.city_to} ({self.fly_to}), {self.country_to['name']}\n" \
               f"Departure: {self.departure_date}\n" \
               f"Nights at destination: {self.nights_in_dest}\n" \
               f"Price: {self.price}\n" \
               f"Book now at: {self.deep_link}\n" \
               f"***************************************************************************************************\n"

    def __lt__(self, other):
        return self.departure_date < other.departure_date
