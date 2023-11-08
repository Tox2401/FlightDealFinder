class Flight:

    def __init__(self, flying_from, city_from, country_from, flying_to, city_to, country_to, departure, nights, price, link):
        format_date = departure.split("T")
        self.flying_from = flying_from
        self.city_from = city_from
        self.country_from = country_from
        self.formatted_from = f"{city_from} ({flying_from}), {country_from['name']}"
        self.flying_to = flying_to
        self.city_to = city_to
        self.country_to = country_to
        self.formatted_to = f"{city_to} ({flying_to}), {country_to['name']}"
        self.departure_date = format_date[0]
        self.departure_time = format_date[1]
        self.nights_at_destination = nights
        self.price = price
        self.deep_link = link

    def __str__(self):
        return f"***************************************************************************************************\n"\
               f"Flying from: {self.city_from} ({self.flying_from}), {self.country_from['name']}\n" \
               f"Flying to: {self.city_to} ({self.flying_to}), {self.country_to['name']}\n" \
               f"Departure: {self.departure_date}\n" \
               f"Nights at destination: {self.nights_at_destination}\n" \
               f"Price: {self.price}\n" \
               f"Book now at: {self.deep_link}\n" \
               f"***************************************************************************************************\n"

    def __lt__(self, other):
        return self.departure_date < other.departure_date
