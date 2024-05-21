import requests
import json

class DuoAPI:
    def __init__(self):
        self.baseURL = "https://www.duolingo.com/api/1/"
        self.username = ""
        self.password = ""
        self.jwt_token = ""
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.login()

    def login(self):
        self.username = input("Type your username:")
        self.password = input("Type your password:")
        self.jwt_token = input("Type your JWT Token (https://github.com/KartikTalwar/Duolingo/issues/128):")
        
        print("Authenticating...")

        resp = requests.get("https://www.duolingo.com/login", {"login":self.username, "password":self.password}, headers={
            "User-Agent":self.user_agent
        })

        print("Obtained response, status code " + str(resp.status_code) + " - " + resp.reason)
        
        if resp.status_code == 200:
            print("Logged in successfully.\n")
            return

        exit("Error: failed to login")

    def get_version_info(self):
        url = "version_info"
        print("Requesting from " + self.baseURL + url + "...")
        resp = requests.get(self.baseURL + url, headers={
            "User-Agent":self.user_agent
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason)
        print("Content:")
        print(resp.text)
        print()
    
    def get_user_data(self):
        url = "users/show?username=" + self.username
        print("Requesting from " + self.baseURL + url + "...")
        resp = requests.get(self.baseURL + url, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.jwt_token
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason)
        info = resp.json()

        print("Content:\n\n")
        print("User: " + info["username"])
        print("Full Name: " + info["fullname"])
        print("Avatar Link: " + info["avatar"] + "\n\n")
        print("Current Language: " + info["learning_language_string"])
        print("Streak: " + str(info["site_streak"]))
        print("Followers: " + str(info["tracking_properties"]["num_followers"]))
        print("Following: " + str(info["tracking_properties"]["num_following"]) + "\n\n")
        print("Languages:")
        for i in info["languages"]:
            if i["learning"] == False:
                continue

            if i["current_learning"] == False:
                print(" - " + i["language_string"])
            else:
                print(" - " + i["language_string"] + " (currently learning)")
    
    def get_current_lang(self):
        url = "users/show?username=" + self.username
        print("Requesting from " + self.baseURL + url + "...")
        resp = requests.get(self.baseURL + url, headers={
            "User-Agent":self.user_agent,
            "Cookie":"jwt_token=" + self.jwt_token
        })

        print("Response obtained:")
        print("Code: " + str(resp.status_code) + " - " + resp.reason)
        info = resp.json()
        cur_lang = info["learning_language"]

        print("Content:\n\n")
        print("Language: " + info["language_data"][cur_lang]["language_string"])

if __name__ == "__main__":
    run = True
    print("Duolingo API: messing around")
    base = DuoAPI()

    while run == True:
        prompt = input("Type the command:")
        if (prompt == "exit"):
            run = False
        elif(prompt == "get_version_info"):
            base.get_version_info()
        elif(prompt == "get_user_data"):
            base.get_user_data()
        elif(prompt == "get_current_lang"):
            base.get_current_lang()