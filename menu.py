class Menu:
    def __init__(self, options):
        self.options = options
        self.opt_amount = len(options)
        self.select = ""
        self.state = 0 # 0 - Inputting, 1 - Success, 2 - Failed
        self.reason = ""

    def query(self):
        self.select = ""
        self.state = 0

        print("\n\nSelect one of the following:")
        for i in range(self.opt_amount):
            print(str(i + 1) + ". " + self.options[i])
            
        self.select = input("\n.: ")

        if (not self.select.isdigit()):
            self.state = 2
            self.reason = "Invalid option selected"
            return
        
        if (int(self.select) < 0 or int(self.select) >= (self.opt_amount + 1)):
            self.state = 2
            self.reason = "Invalid option selected"
            return

        self.state = 1