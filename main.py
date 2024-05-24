#https://www.duolingo.com/2017-06-30/login
#https://simg-ssl.duolingo.com
#https://www.duolingo.com/lesson?id=<lesson_id>
import requests
import json
import datetime
from menu import Menu

class DuoAPI:
    def __init__(self):
        self.baseURL = "https://www.duolingo.com/api/1/"
        self.export_dir = "export/"

        self.username = ""
        self.password = ""
        self.jwt_token = ""
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

        try:
            qjwt = open(self.export_dir + "jwt_token","r")
            self.jwt_token = qjwt.read()
            print("Authenticated successfully, if you want to change user, login into a different account on duolingo.com and use the Authenticate option.")
        except OSError:
            print("Some options require authentication, please use the Authenticate option in the menu to authenticate.\n")

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

        user_data = [
            "=== INFO ===",
            "\nUser: " + resp_data["name"],
            "\nUsername: " + resp_data["username"],
            "\nUser ID: " + str(resp_data["id"]),
            "\nDescription: " + resp_data["bio"],
            "\n\n=== STREAK ===",
            "\nCurrent Streak: " + str(resp_data["streak"]),
            "\nStart Date (YYYY-MM-DD): " + resp_data["streakData"]["currentStreak"]["startDate"],
            "\n\n=== COURSES ===",
            "\nCurrent Course: " + resp_data["courses"][0]["title"] + " (" + resp_data["fromLanguage"] + ")",
            "\nCourse ID: " + resp_data["currentCourseId"],
            "\n\nAll courses:"
        ]

        for i in resp_data["courses"]:
            user_data.append("\n " + i["title"] + " (" + i["fromLanguage"] + ")")
            user_data.append("\n  ID: " + str(i["id"]))
            user_data.append("\n  Crowns: " + str(i["crowns"]))
            user_data.append("\n  XP: " + str(i["xp"]) + "\n")

        if resp_data["hasPlus"] == False:
            user_data.insert(5, "\nDuolingo Free")
        else:
            user_data.append(5, "\nDuolingo Plus")

        fexp = open(self.export_dir + "user_data.txt", "w")
        fexp.writelines(user_data)
        fexp.close()

        for i in user_data:
            print(i, end="")

    def get_user_following(self):
        url = "https://www.duolingo.com/2017-06-30/friends/users/"
        url_append = "/following"

        url_user = "https://www.duolingo.com/2017-06-30/users?username="

        print("Requesting from " + url_user + self.username + "...")
        resp = requests.get(url_user + self.username, headers={
            "User-Agent":self.user_agent,
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        first_resp_json = json.loads(resp.text)
        user_id = str(first_resp_json["users"][0]["id"])

        print("Requesting from " + url + user_id + url_append + "...")
        resp = requests.get(url + user_id + url_append, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.jwt_token
        })

        print("Content:")
        #print(resp.text)
        resp_json = json.loads(resp.text)
        
        user_follow = [
            "=== Users following " + self.username + " ==="
        ]
        for i in resp_json["following"]["users"]:
            user_follow.append("\n" + i["displayName"])
            user_follow.append("\n Username: " + i["username"])
            user_follow.append("\n ID: " + str(i["userId"]))
            
            if i["isFollowedBy"] == True:
                user_follow.append("\n Follows Back")
            
            if i["hasSubscription"] == True:
                user_follow.append("\n Duolingo Plus")
            else:
                user_follow.append("\n Duolingo Free")
            
            if i["isCurrentlyActive"] == True:
                user_follow.append("\n Currently Online")
            else:
                user_follow.append("\n Currently Offline")
            
            user_follow.append("\n Total XP: " + str(i["totalXp"]) + "\n")
        
        fexp = open(self.export_dir + "followers_" + user_id + ".txt","w")
        fexp.writelines(user_follow)
        fexp.close()

        print("Contents written to /exports")

        #for i in user_follow:
        #    print(i, end="")

    def get_store_items(self):
        url = "https://www.duolingo.com/2017-06-30/shop-items"
        print("Requesting from " + url + "...")
        resp = requests.get(url, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.jwt_token
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        print("Content:")
        resp_json = json.loads(resp.text)

        store_stuff = [
            "=== All Store Items ==="
        ]

        for i in resp_json["shopItems"]:
            if "name" in i.keys():
                store_stuff.append("\n" + i["name"])
            else:
                store_stuff.append("\nHidden Item")
            
            store_stuff.append("\n ID: " + i["id"])
            store_stuff.append("\n Type: " + i["type"])

            if "currencyType" in i:
                store_stuff.append("\n Price: " + i["currencyType"] + " " + str(i["price"]))
            
            if "lastUsedDate" in i:
                store_stuff.append("\n Last Used: " + str(datetime.datetime.fromtimestamp(i["lastUsedDate"])))
        
            store_stuff.append("\n")
        
        fexp = open(self.export_dir + "store.txt","w")
        fexp.writelines(store_stuff)
        fexp.close()

        print("Contents written to /exports")

    def get_user_achievements(self):
        url = "https://duolingo-achievements-prod.duolingo.com/users/<user_id>/achievements?fromLanguage=<fromLanguage>&learningLanguage=<learningLanguage>"
        print("Requesting from " + url + "...")
        resp = requests.get(url, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.jwt_token
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        print("Content:")
        resp_json = json.loads(resp.text)

        store_stuff = [
            "=== All Store Items ==="
        ]

        for i in resp_json["shopItems"]:
            if "name" in i.keys():
                store_stuff.append("\n" + i["name"])
            else:
                store_stuff.append("\nHidden Item")
            
            store_stuff.append("\n ID: " + i["id"])
            store_stuff.append("\n Type: " + i["type"])

            if "currencyType" in i:
                store_stuff.append("\n Price: " + i["currencyType"] + " " + str(i["price"]))
            
            if "lastUsedDate" in i:
                store_stuff.append("\n Last Used: " + str(datetime.datetime.fromtimestamp(i["lastUsedDate"])))
        
            store_stuff.append("\n")
        
        fexp = open(self.export_dir + "store.txt","w")
        fexp.writelines(store_stuff)
        fexp.close()

        print("Contents written to /exports")

if __name__ == "__main__":
    run = True
    base = DuoAPI()

    main_menu = Menu([
        "Exit",
        "Authenticate",
        "Version Info (no auth)",
        "Public User Data (no auth)",
        "Get User Following (auth)",
        "Get Store Items (auth)",
        "Get User Achivements (auth)"
        # https://duolingo-achievements-prod.duolingo.com/users/<user_id>/achievements?fromLanguage=<fromLanguage>&learningLanguage=<learningLanguage>
    ])

    print("Duolingo API: messing around")

    while run == True:
        main_menu.query()
        if main_menu.state == 1:
            if main_menu.select == "1":
                run = False
                break
            elif main_menu.select == "2":
                base.jwt_token = input("To authenticate, please type your jwt_token cookie (https://github.com/KartikTalwar/Duolingo/issues/128):\n")
                tf = open(base.export_dir + "jwt_token", "w")
                tf.write(base.jwt_token)
                tf.close()
                continue
            elif main_menu.select == "3":
                base.get_version_info()
                continue
            elif main_menu.select == "4":
                base.username = input("Type the username: ")
                base.get_public_user()
                continue
            elif main_menu.select == "5":
                base.username = input("Type the username: ")
                base.get_user_following()
                continue
            elif main_menu.select == "6":
                base.get_store_items()
                continue
            elif main_menu.select == "7":
                base.get_user_achievements()
                continue
        print("Error: " + main_menu.reason)