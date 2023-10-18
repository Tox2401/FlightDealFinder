from tkinter import *
from FlightSearch import search
from DataManager import showSearchHistory, clearSearchHistory


masterWindow = Tk()
masterWindow.title("Flight Deal Finder")
masterWindow.geometry("350x550")
masterWindow.config(padx=10, pady=10)

canvas = Canvas(width=320, height=320, highlightthickness=0)
logoImg = PhotoImage(file="data/logo.png")
canvas.create_image(160, 160, image=logoImg)
canvas.grid(column=0, row=0, columnspan=4)

departureAirportLabel = Label(text="Departure airport:")
departureAirportLabel.grid(column=0, row=1, columnspan=1, sticky="E")

fromAirportInput = Entry()
fromAirportInput.insert(0, "E.g. Zagreb")
fromAirportInput.bind("<FocusIn>",
                      lambda event: fromAirportInput.delete(0, "end") if fromAirportInput.get() == "E.g. Zagreb" else None)
fromAirportInput.bind("<FocusOut>",
                      lambda event: fromAirportInput.insert(0, "E.g. Zagreb") if fromAirportInput.get() == "" else None)
fromAirportInput.grid(column=1, row=1, columnspan=3, sticky="EW")

destinationAirportLabel = Label(text="Destination airport/s:")
destinationAirportLabel.grid(column=0, row=2, columnspan=1, sticky="E")

toAirportInput = Entry()
toAirportInput.insert(0, "E.g. Paris, London, Oslo, Athens")
toAirportInput.bind("<FocusIn>",
                    lambda event: toAirportInput.delete(0, "end") if toAirportInput.get() == "E.g. Paris, London, Oslo, Athens" else None)
toAirportInput.bind("<FocusOut>",
                    lambda event: toAirportInput.insert(0, "E.g. Paris, London, Oslo, Athens") if toAirportInput.get() == "" else None)
toAirportInput.grid(column=1, row=2, columnspan=3, sticky="EW")

fromDateLabel = Label(text="Date from:")
fromDateLabel.grid(column=0, row=3, columnspan=1, sticky="E")

fromDateEntry = Entry()
fromDateEntry.insert(0, "dd/mm/yyyy (E.g. 15/12/2023)")
fromDateEntry.bind("<FocusIn>",
                    lambda event: fromDateEntry.delete(0, "end") if fromDateEntry.get() == "dd/mm/yyyy (E.g. 15/12/2023)" else None)
fromDateEntry.bind("<FocusOut>",
                    lambda event: fromDateEntry.insert(0, "dd/mm/yyyy (E.g. 15/12/2023)") if fromDateEntry.get() == "" else None)
fromDateEntry.grid(column=1, row=3, columnspan=3, sticky="EW")

toDateLabel = Label(text="Date to:")
toDateLabel.grid(column=0, row=4, columnspan=1, sticky="E")

toDateEntry = Entry()
toDateEntry.insert(0, "dd/mm/yyyy (E.g. 15/01/2024)")
toDateEntry.bind("<FocusIn>",
                    lambda event: toDateEntry.delete(0, "end") if toDateEntry.get() == "dd/mm/yyyy (E.g. 15/01/2024)" else None)
toDateEntry.bind("<FocusOut>",
                    lambda event: toDateEntry.insert(0, "dd/mm/yyyy (E.g. 15/01/2024)") if toDateEntry.get() == "" else None)
toDateEntry.grid(column=1, row=4, columnspan=3, sticky="EW")

maxStopoversLabel = Label(text="Max stopovers:")
maxStopoversLabel.grid(column=0, row=5, columnspan=1, sticky="E")


stopoverOptions = ["0", "1", "2", "3", "4", "5"]
stopovers = None


def getMaxStopovers(choice):
    global stopovers
    stopovers = int(choice)


maxStopoversOptionMenu = OptionMenu(masterWindow, StringVar(), *stopoverOptions, command=getMaxStopovers)
maxStopoversOptionMenu.grid(column=1, row=5, columnspan=1, sticky="W")

stayDurationLabel = Label(text="Nights at destination:")
stayDurationLabel.grid(column=0, row=6, columnspan=1, sticky="E")

minNightsEntry = Entry(width=6)
minNightsEntry.insert(0, "E.g. 7")
minNightsEntry.bind("<FocusIn>",
                    lambda event: minNightsEntry.delete(0, "end") if minNightsEntry.get() == "E.g. 7" else None)
minNightsEntry.bind("<FocusOut>",
                    lambda event: minNightsEntry.insert(0, "E.g. 7") if minNightsEntry.get() == "" else None)
minNightsEntry.grid(column=1, row=6, columnspan=1, sticky="E")

toDurationLabel = Label(text="-", width=2)
toDurationLabel.grid(column=2, row=6, columnspan=1)

maxNightsEntry = Entry(width=6)
maxNightsEntry.insert(0, "E.g. 14")
maxNightsEntry.bind("<FocusIn>",
                    lambda event: maxNightsEntry.delete(0, "end") if maxNightsEntry.get() == "E.g. 14" else None)
maxNightsEntry.bind("<FocusOut>",
                    lambda event: maxNightsEntry.insert(0, "E.g. 14") if maxNightsEntry.get() == "" else None)
maxNightsEntry.grid(column=3, row=6, columnspan=1, sticky="W")

searchBtn = Button(text="Search", command=lambda: search(departure=fromAirportInput.get(),
                                                         destinations=toAirportInput.get(),
                                                         fromDate=fromDateEntry.get(),
                                                         toDate=toDateEntry.get(),
                                                         maxStopovers=stopovers,
                                                         minNights=int(minNightsEntry.get()),
                                                         maxNights=int(maxNightsEntry.get())))
searchBtn.grid(column=0, row=7, columnspan=4, sticky="EW")

searchBtn = Button(text="Search history", command=lambda: showSearchHistory(masterWindow))
searchBtn.grid(column=0, row=8, columnspan=4, sticky="EW")
searchBtn = Button(text="Clear history", command=lambda: clearSearchHistory())
searchBtn.grid(column=0, row=9, columnspan=4, sticky="EW")


masterWindow.mainloop()
