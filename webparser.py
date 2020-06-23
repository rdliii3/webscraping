from bs4 import BeautifulSoup

class webparser():
    
    def __init__(self,html,parse_type):
        self.document=BeautifulSoup(html,'lxml')
        self.parse_type=parse_type
        self.functions={'print':self.printHtml,
                        'table':self.parseTable,
                        'tableTree':self.parseTableTree}        
        self.setup()

    def setup(self):
        self.parse=self.functions[self.parse_type]

    def printHtml(self):
        print(self.document.prettify())

    def parseTable(self):
        data=[]
        #navigate the table row by row and save all strings to data list
        table=self.document.tbody
        rows=table.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            csv_row=[]
            for col in cols:
                for string in col.stripped_strings:
                    csv_row.append(string)
            data.append(csv_row)
        return data

    def parseTableTree(self):
        data=[]
        self.document.prettify()
        tables=self.document.find_all('table')
        i = 0
        for table in tables:
            i += 1
            tableParser=webparser(str(table),'table')
            one_table_data = tableParser.parse()
            # add identifying info to table data
            for line in one_table_data:
                line.insert(0, str(i))
            data += one_table_data
        return data
    

if __name__=='__main__':
    webparser('<html>This is a unit test for printing html contents</html>','print')
