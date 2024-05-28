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
        self.save_json = False

        self.admin = ""
        self.token = ""
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

        self.saved_users = []

        try:
            qjwt = open(self.export_dir + "jwt_token","r")
            self.token = qjwt.read()
            print("Authenticated successfully, if you want to change user, login into a different account on duolingo.com and use the 'Authenticate' option.")
        except OSError:
            print("Your user token is required in order to use the API, please use the 'Authenticate' option in the menu.\n")

    def get_public_user(self, user=None, get="all"):
        url = "https://www.duolingo.com/2017-06-30/users?username="

        if user == None:
            user = self.admin

        print("Requesting from " + url + user + "...")
        resp = requests.get(url + user, headers={
            "User-Agent":self.user_agent
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")

        if resp.status_code != 200:
            print("ERROR: Request failed.")
            return

        print("Content:")
        resp_json = json.loads(resp.text)
        #print(resp_json)
        resp_data = resp_json["users"][0]

        if get == "all":
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
        
        print("Information saved to file.")

    def get_user_following(self):
        url = "https://www.duolingo.com/2017-06-30/friends/users/"
        url_append = "/following"

        url_user = "https://www.duolingo.com/2017-06-30/users?username="

        print("Requesting from " + url_user + self.admin + "...")
        resp = requests.get(url_user + self.admin, headers={
            "User-Agent":self.user_agent,
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason + "\n")
        first_resp_json = json.loads(resp.text)
        user_id = str(first_resp_json["users"][0]["id"])

        print("Requesting from " + url + user_id + url_append + "...")
        resp = requests.get(url + user_id + url_append, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.token
        })

        print("Content:")
        #print(resp.text)
        resp_json = json.loads(resp.text)
        
        user_follow = [
            "=== Users following " + self.admin + " ==="
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
            "Cookie":"jwt_token=" + self.token
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
            "Cookie":"jwt_token=" + self.token
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
        "Get User Data",
        "Get User Following",
        "Get Store Items",
        "Get User Achivements"
        # https://duolingo-achievements-prod.duolingo.com/users/<user_id>/achievements?fromLanguage=<fromLanguage>&learningLanguage=<learningLanguage>
    ])

    public_data_menu = Menu([
        "Back",
        "Write All to File"
    ])

    select_user_menu = Menu([
        "Cancel",
        "Use Current User",
        "Use Saved User",
        "Use Custom User"
    ])

    print("Duolingo API: messing around")

    while run == True:
        main_menu.query()
        if main_menu.state == 1:
            if main_menu.select == "1":
                run = False
                break
            elif main_menu.select == "2":
                base.admin = input("Please type your Duolingo username: ")
                base.token = input("To authenticate, please type your jwt_token cookie (https://github.com/KartikTalwar/Duolingo/issues/128):\n")
                tf = open(base.export_dir + "jwt_token", "w")
                tf.write(base.token)
                tf.close()
                continue
            elif main_menu.select == "3":
                select_user_menu.query()
                if select_user_menu.state == 1 and main_menu.select == "1":
                    continue
                
                public_data_menu.query()
                if public_data_menu.state == 1:
                    if public_data_menu.select == "1":
                        continue
                    elif public_data_menu.select == "2":
                        if select_user_menu.select == "2":
                            base.get_public_user()
                        elif select_user_menu.select == "3":
                            print("TBA")
                            continue
                        elif select_user_menu.select == "4":
                            base.get_public_user(input("Enter username: "))
                continue
            elif main_menu.select == "4":
                base.get_user_following()
                continue
            elif main_menu.select == "5":
                base.get_store_items()
                continue
            elif main_menu.select == "6":
                base.get_user_achievements()
                continue
        print("Error: " + main_menu.reason)