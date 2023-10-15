# import requests
# import pandas
# from datetime import datetime, timedelta
# from NotificationManager import NotificationManager
# import os
#
# class DataManager:
#
# while True:
#     registrationPrompt = input("Do you want to register and receive updates for latest cheap flights? (Y/N): ")
#
#     if registrationPrompt.upper() == "Y":
#         NotificationManager.addUser()
#
#     elif registrationPrompt.upper() == "N":
#         break
#
#     else:
#         print("Invalid input, try again (Enter Y/N) ")
#
#     while True:
#         anotherUserPrompt = input("Do you want to add another user? (Y/N): ")
#         if anotherUserPrompt.upper() == "Y":
#             NotificationManager.addUser()
#         elif anotherUserPrompt.upper() == "N":
#             break
#         else:
#             print("Invalid input, try again (Enter Y/N) ")
#
#     break
