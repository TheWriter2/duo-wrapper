#https://www.duolingo.com/2017-06-30/login
import requests
import json
from menu import Menu

class DuoAPI:
    def __init__(self):
        self.baseURL = "https://www.duolingo.com/api/1/"
        self.username = ""
        self.password = ""
        self.jwt_token = ""
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    def get_version_info(self):
        url = "version_info"
        print("Requesting from " + self.baseURL + url + "...")
        resp = requests.get(self.baseURL + url, headers={
            "User-Agent":self.user_agent
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        print("Content:")
        for i in resp.json().items():
            print(i)

    def get_public_user(self):
        url = "https://www.duolingo.com/2017-06-30/users?username="
        print("Requesting from " + url + self.username + "...")
        resp = requests.get(url + self.username, headers={
            "User-Agent":self.user_agent
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        print("Content:")
        resp_json = json.loads(resp.text)
        #print(resp_json)
        resp_data = resp_json["users"][0]

        print("=== INFO ===")
        print("User: " + resp_data["name"])
        print("Username: " + resp_data["username"])
        print("User ID: " + str(resp_data["id"]))
        print("Description: " + resp_data["bio"])
        if resp_data["hasPlus"] == False:
            print("Duolingo Free")
        else:
            print("Duolingo Plus")

        print("\n=== STREAK ===")
        print("Current Streak: " + str(resp_data["streak"]))
        print("Start Date (YYYY-MM-DD): " + resp_data["streakData"]["currentStreak"]["startDate"])

        print("\n=== COURSES ===")
        print("Current Course: " + resp_data["courses"]["0"]["title"] + " (" + resp_data["fromLanguage"] + ")")
        print("Course ID: " + resp_data["currentCourseId"])
        print("\nAll courses:")
        for i in resp_data["courses"]:
            print(" " + i["title"] + " (" + i["fromLanguage"] + ")")
            print("  ID: " + str(i["id"]))
            print("  Crowns: " + str(i["crowns"]))
            print("  XP: " + str(i["xp"]) + "\n")

if __name__ == "__main__":
    run = True
    base = DuoAPI()

    main_menu = Menu([
        "Exit",
        "Version Info (no auth)",
        "Public User Data (no auth)"
    ])

    print("Duolingo API: messing around")

    while run == True:
        main_menu.query()
        if main_menu.state == 1:
            if main_menu.select == "1":
                run = False
                break
            elif main_menu.select == "2":
                base.get_version_info()
                continue
            elif main_menu.select == "3":
                base.username = input("Type the username: ")
                base.get_public_user()
                continue
        print("Error: " + main_menu.reason)