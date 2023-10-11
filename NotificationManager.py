import json
import os
import smtplib


class NotificationManager:

    @staticmethod
    def addUser():  # Checking for existing user implementation pending

        while True:
            fName = input("Enter your first name: ")
            lName = input("Enter your last name: ")
            email = input("Enter your email: ")

            users = {
                email: {
                    "fName": fName.title(),
                    "lName": lName.title(),
                    "email": email.lower(),
                }
            }

            while True:
                confirmation = input("Is this information correct?\n"
                                     f"First name: {fName}\n"
                                     f"Last name: {lName}\n"
                                     f"Email: {email}\n"
                                     f"Y/N: ")

                if confirmation.upper() == "Y":
                    try:
                        with open("data/users.json", "r") as jsonData:
                            usersData = json.load(jsonData)
                            usersData.update(users)
                            with open("data/users.json", "w") as jsonData:
                                json.dump(usersData, jsonData, indent=4)

                        break

                    except FileNotFoundError:
                        with open("data/users.json", "w") as jsonData:
                            json.dump(users, jsonData, indent=4)

                        break

                elif confirmation.upper() == "N":
                    break

                else:
                    print("Invalid input.")
                    pass

            if confirmation.upper() == "Y":
                break
            else:
                pass

    @staticmethod
    def notifyUsers(message):
        pass    # Write code for sending email to all users inside users.json
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=os.environ.get("EMAIL"), password=os.environ.get("EMAIL_PASS"))

        try:
            with open("data/users.json", "r") as jsonData:
                usersData = json.load(jsonData)
                for key in usersData:
                    connection.sendmail(from_addr=os.environ.get("EMAIL"),
                                        to_addrs=usersData[key]["email"],
                                        msg=f"Subject: >>SUBJECT<<\n\n{message}")
        except FileNotFoundError:
            print("No users in database")

        connection.close()
