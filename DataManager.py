import sqlite3
from tkinter import *
import tkinter.messagebox
import pyperclip

def showSearchHistory(masterWindow):
    searchHistoryWindow = Toplevel(masterWindow)
    searchHistoryWindow.title("Search history")
    searchHistoryWindow.geometry("200x400")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    searchResults = []

    for table in cursor.execute("select name from sqlite_master where type='table' order by name"):
        searchResults.append(table)

    searchResults.reverse()

    for result in searchResults:
        timestamp = result[0].split("_")
        Button(searchHistoryWindow, text=f"{timestamp[1]} - {timestamp[2]}",
               command=lambda: showResult(searchHistoryWindow, cursor, result)).pack(pady=1)


def showResult(window, cursor, table):
    resultWindow = Toplevel(window)
    resultWindow.title("Results")
    resultWindow.geometry("200x400")
    for row in cursor.execute(f"select * from '{table[0]}'"):
        Label(resultWindow, text=f"From: {row[0]}\n"
                                 f"To: {row[1]}\n"
                                 f"Departure: {row[2]} / {row[3]}\n"
                                 f"Stay: {row[4]} nights\n"
                                 f"Price: {row[5]} EUR").pack(pady=2)
        Button(resultWindow, text="Book now", command=lambda row=row[6]: booking(row)).pack()

    def booking(link):
        pyperclip.copy(link)
        tkinter.messagebox.showinfo(message="Booking link has been copied to the clipboard.")


def clearSearchHistory():
    confirmation = tkinter.messagebox.askokcancel(title="Confirmation",
                                                  message="Are you sure you want to delete all of your search history?")
    if confirmation:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        tables = []
        for table in cursor.execute("select name from sqlite_master where type='table' order by name"):
            tables.append(table)
        for table in tables:
            cursor.execute(f"drop table '{table[0]}'")
        connection.commit()
        tkinter.messagebox.showinfo(message="Search history has been deleted.")
    else:
        pass
