import shelve


class databaseManager:

    def __init__(self, dbLocation):
        self.dbLocation =dbLocation
        

    def saveLevelOutput(self, ID, file):
        self.db = shelve.open(self.dbLocation, flag = 'c', protocol=None, writeback = False)
        self.db[ID] = file
        self.db.close()
        print(ID + " Output saved")

    def checkDbEntry(self,ID):
        self.db = shelve.open(self.dbLocation, flag = 'c', protocol=None, writeback = False)
        if ID in list(self.db.keys()):
            self.db.close()
            return True
        else:
            self.db.close()
            return False

    def getDbEntry(self,ID):
        self.db = shelve.open(self.dbLocation, flag = 'c', protocol=None, writeback = False)
        output = self.db.get(ID)
        self.db.close()
        return output



