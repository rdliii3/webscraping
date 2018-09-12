from bs4 import BeautifulSoup

class webparser():
    
    def __init__(self,html,parse_type):
        self.document=BeautifulSoup(html,'lxml')
        self.parse_type=parse_type
        self.functions={'print':self.printHtml,
                        'table':self.parseTable}
        self.setup()
        self.parse()

    def setup(self):
        self.parse=self.functions[self.parse_type]

    def printHtml(self):
        print(self.document.prettify())

    def parseTable(self):
        pass
        
    

if __name__=='__main__':
    webparser('<html>This is a unit test for printing html contents</html>','print')
