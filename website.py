import os,sys
import base64
import pickle
from getpass import getpass

class website:

    def __init__(self,url):
        '''Initializes a website object to the provided url'''
        self.url='https://'+url
        self.baseDir=os.getenv('HOME')
        self.retrieve()
        self.save()

    def save(self):
        '''Save data to a pickle file'''
        if not os.path.exists(self.baseDir+"/.web"):
            os.mkdir(self.baseDir+'/.web')
        if os.path.exists(self.baseDir+'/.web/saved.p'):
            with open(self.baseDir+'/.web/saved.p', 'r+b') as fin:
                data = pickle.load(fin)
                data[self.url] = [base64.b64encode(bytes(self.__username,'ascii')),base64.b64encode(bytes(self.__password,'ascii'))]
                fin.seek(0)
                fin.truncate()
                pickle.dump(data,fin)

        else:
            with open(self.baseDir+'/.web/saved.p', 'wb') as fin:
                data={}
                data[self.url] = [base64.b64encode(bytes(self.__username,'ascii')),base64.b64encode(bytes(self.__password,'ascii'))]
                pickle.dump( data, fin )


    def retrieve(self):
        '''Retrieve data associated with the website if it exists.
        Otherwise prompt the user for the data.'''
        
        if os.path.exists(self.baseDir+'/.web/saved.p'):
            with open(self.baseDir+'/.web/saved.p', 'rb') as fin:
                data=pickle.load(fin)
                if self.url in data:
                    self.__username = str(base64.b64decode(data[self.url][0]),'ascii')
                    self.__password = str(base64.b64decode(data[self.url][1]),'ascii')
                else:
                    self.__username=self.ask_username()
                    self.__password=getpass("Enter the password associated with the username:")
        else:
            self.__username=self.ask_username()
            self.__password=getpass("Enter the password associated with the username:")

    def ask_username(self):
        return input("Enter the username associated with the website:")

    def username(self):
        return self.__username

    def password(self):
        return self.__password
        

if __name__ == "__main__":
    print("Unit test of website class")
    test1 = website("DummyURL")
    print("URL="+test1.url)
    print("Username="+test1.username())
    print("Password="+test1.password())
    test2 = website("DummyURL")
    print("URL="+test2.url)
    print("Username="+test2.username())
    print("Password="+test2.password())
