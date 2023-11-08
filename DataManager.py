import sqlite3
from tkinter import *
import tkinter.messagebox
import pyperclip


def create_scrollbar_frame(window):

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas = Canvas(window, width=200, height=400)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    return frame


def show_search_history(master_window):
    search_history_window = Toplevel(master_window)
    search_history_window.title("Search history")
    search_history_window.geometry("130x400")
    search_history_frame = create_scrollbar_frame(search_history_window)

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    search_results = []

    for table in cursor.execute("select name from sqlite_master where type='table' order by name"):
        search_results.append(table)

    search_results.reverse()

    for result in search_results:
        timestamp = result[0].split("_")
        Button(search_history_frame, text=f"{timestamp[1]} - {timestamp[2]}",
               command=lambda: show_result(search_history_frame, cursor, result)).pack(pady=1)


def show_result(master_window, cursor, table):
    result_window = Toplevel(master_window)
    result_window.title("Results")
    result_window.geometry("220x400")
    result_window_frame = create_scrollbar_frame(result_window)

    for row in cursor.execute(f"select * from '{table[0]}'"):
        Label(result_window_frame, text=f"From: {row[0]}\n"
                                 f"To: {row[1]}\n"
                                 f"Departure: {row[2]} / {row[3]}\n"
                                 f"Stay: {row[4]} nights\n"
                                 f"Price: {row[5]} EUR").pack(pady=2)
        Button(result_window_frame, text="Book now", command=lambda row=row[6]: booking(row)).pack()

    def booking(link):
        pyperclip.copy(link)
        tkinter.messagebox.showinfo(message="Booking link has been copied to the clipboard.")


def clear_search_history():
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
