from tkinter import *
from FlightSearch import search
from DataManager import show_search_history, clear_search_history


def get_max_stopovers():
    stopovers = stopovers_choice.get()
    return stopovers


master_window = Tk()
master_window.title("Flight Deal Finder")
master_window.geometry("350x550")
master_window.config(padx=10, pady=10)

canvas = Canvas(width=320, height=320, highlightthickness=0)
logoImg = PhotoImage(file="data/logo.png")
canvas.create_image(160, 160, image=logoImg)
canvas.grid(column=0, row=0, columnspan=4)

departure_airport_label = Label(text="Departure airport:")
departure_airport_label.grid(column=0, row=1, columnspan=1, sticky="E")

departure_airport_input = Entry()
departure_airport_input.insert(0, "E.g. Zagreb")
departure_airport_input.bind("<FocusIn>",
                             lambda event: departure_airport_input.delete(0, "end") if departure_airport_input.get() == "E.g. Zagreb" else None)
departure_airport_input.bind("<FocusOut>",
                             lambda event: departure_airport_input.insert(0, "E.g. Zagreb") if departure_airport_input.get() == "" else None)
departure_airport_input.grid(column=1, row=1, columnspan=3, sticky="EW")

destination_airport_label = Label(text="Destination airport/s:")
destination_airport_label.grid(column=0, row=2, columnspan=1, sticky="E")

destination_airport_input = Entry()
destination_airport_input.insert(0, "E.g. Paris, London, Oslo, Athens")
destination_airport_input.bind("<FocusIn>",
                               lambda event: destination_airport_input.delete(0, "end") if destination_airport_input.get() == "E.g. Paris, London, Oslo, Athens" else None)
destination_airport_input.bind("<FocusOut>",
                               lambda event: destination_airport_input.insert(0, "E.g. Paris, London, Oslo, Athens") if destination_airport_input.get() == "" else None)
destination_airport_input.grid(column=1, row=2, columnspan=3, sticky="EW")

from_date_label = Label(text="Date from:")
from_date_label.grid(column=0, row=3, columnspan=1, sticky="E")

from_date_entry = Entry()
from_date_entry.insert(0, "dd/mm/yyyy (E.g. 15/12/2023)")
from_date_entry.bind("<FocusIn>",
                     lambda event: from_date_entry.delete(0, "end") if from_date_entry.get() == "dd/mm/yyyy (E.g. 15/12/2023)" else None)
from_date_entry.bind("<FocusOut>",
                     lambda event: from_date_entry.insert(0, "dd/mm/yyyy (E.g. 15/12/2023)") if from_date_entry.get() == "" else None)
from_date_entry.grid(column=1, row=3, columnspan=3, sticky="EW")

to_date_label = Label(text="Date to:")
to_date_label.grid(column=0, row=4, columnspan=1, sticky="E")

to_date_entry = Entry()
to_date_entry.insert(0, "dd/mm/yyyy (E.g. 15/01/2024)")
to_date_entry.bind("<FocusIn>",
                   lambda event: to_date_entry.delete(0, "end") if to_date_entry.get() == "dd/mm/yyyy (E.g. 15/01/2024)" else None)
to_date_entry.bind("<FocusOut>",
                   lambda event: to_date_entry.insert(0, "dd/mm/yyyy (E.g. 15/01/2024)") if to_date_entry.get() == "" else None)
to_date_entry.grid(column=1, row=4, columnspan=3, sticky="EW")

max_stopovers_label = Label(text="Max stopovers:")
max_stopovers_label.grid(column=0, row=5, columnspan=1, sticky="E")

stopover_options = ["0", "1", "2", "3", "4", "5"]
stopovers_choice = StringVar()
max_stopovers_optionmenu = OptionMenu(master_window, stopovers_choice, *stopover_options)
max_stopovers_optionmenu.grid(column=1, row=5, columnspan=1, sticky="W")

stay_duration_label = Label(text="Nights at destination:")
stay_duration_label.grid(column=0, row=6, columnspan=1, sticky="E")

min_nights_entry = Entry(width=6)
min_nights_entry.insert(0, "E.g. 7")
min_nights_entry.bind("<FocusIn>",
                      lambda event: min_nights_entry.delete(0, "end") if min_nights_entry.get() == "E.g. 7" else None)
min_nights_entry.bind("<FocusOut>",
                      lambda event: min_nights_entry.insert(0, "E.g. 7") if min_nights_entry.get() == "" else None)
min_nights_entry.grid(column=1, row=6, columnspan=1, sticky="E")

to_duration_label = Label(text="-", width=2)
to_duration_label.grid(column=2, row=6, columnspan=1)

max_nights_entry = Entry(width=6)
max_nights_entry.insert(0, "E.g. 14")
max_nights_entry.bind("<FocusIn>",
                      lambda event: max_nights_entry.delete(0, "end") if max_nights_entry.get() == "E.g. 14" else None)
max_nights_entry.bind("<FocusOut>",
                      lambda event: max_nights_entry.insert(0, "E.g. 14") if max_nights_entry.get() == "" else None)
max_nights_entry.grid(column=3, row=6, columnspan=1, sticky="W")

search_button = Button(text="Search", command=lambda: search(departure=departure_airport_input.get(),
                                                             destinations=destination_airport_input.get(),
                                                             from_date=from_date_entry.get(),
                                                             to_date=to_date_entry.get(),
                                                             max_stopovers=get_max_stopovers(),
                                                             min_nights=int(min_nights_entry.get()),
                                                             max_nights=int(max_nights_entry.get())))
search_button.grid(column=0, row=7, columnspan=4, sticky="EW")

show_search_history_button = Button(text="Show search history", command=lambda: show_search_history(master_window))
show_search_history_button.grid(column=0, row=8, columnspan=4, sticky="EW")

clear_search_history_button = Button(text="Clear history", command=lambda: clear_search_history())
clear_search_history_button.grid(column=0, row=9, columnspan=4, sticky="EW")

master_window.mainloop()
