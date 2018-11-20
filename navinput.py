import os, sys

class navinput():
    '''Simple class that parses the instruction input file and provides access to the instructions'''

    def __init__(self,filePath):
        self.delimeter=' '
        self.website=None
        self.instructionFile=filePath




    def setup(self,filePath=None):
        '''Function to parse the input file and check for errors
        Input - filePath = path to file containing instructions
        Result - a list of instructions (each instruction is a list of 4 strings) owned by the navinput object
        '''
        filePath=filePath if filePath is not None else self.instructionFile

        with open(filePath,'r') as fin:
            raw=fin.readlines()
        self.instructions=[]
        self.parse_errors=0
        self.parse(raw)
        self.current_idx=0
        self.QCprintout()
        


    def parse(self,rawList):
        '''Function to parse the text from the instruction file
        Input - list of strings
        Return - None
        Side effect - populate list of instructions
        '''
        for item in rawList:
            line=item.strip()
            if not line:
                continue
            if line[0] == '': #skip empty lines
                continue
            if line[0] == '#': #skip comment lines
                continue

            if line[0] == '@': #website url
                self.processWebsite(line)
            else:
                result=self.processLine(line)
                if isinstance(result,list):
                    self.instructions.append(result)
                else:
                    self.reportError(result,rawList.index(item)+1,line)
        

    def processLine(self,line):
        ''' Function to change an instruction from a raw string to a list usable by a webnavigator object.
        Input - instruction line as a string
        Output - a list of length 4 if the input string is a valid instruction otherwise a
                 a string describing the error
        '''
        l = line.split(self.delimeter)
        #clean input strings
        for i in range(len(l)):
            l[i] = l[i].strip()

        #ensure number of items is correct
        if len(l) == 4:
            return l
        if len(l) == 3: #add empty fourth field
            l.append("")
            return l
        if len(l) < 3:
            # Handle output options
            if l[0].lower() == 'output' or l[0].lower() == 'flush':
                return ["","",l[0].lower(),""]
        if len(l) > 4:
            return 'Error: Too many fields on line'
        return 'Error: Unknown error'

    def processWebsite(self,line):
        '''Function to process a website line from instructions file.
        Input:string
        Return:
        Side-effect: Add website property to object
        '''
        line=line[1:] #strip off '@'
        self.website=line

    def current(self):
        return self.instructions[self.current_idx]

    def next(self):
        if self.current_idx < len(self.instructions) - 1:
            self.current_idx += 1
            return self.current()
        return None

    def previous(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            return self.current()
        return None

    def first(self):
        self.current_idx = 0
        return self.current()


    def last(self):
        self.current_idx = len(self.instructions) - 1
        return self.current()

    def all(self):
        return self.instructions

    def reportError(self,error,line_num,line_text):
        print(error)
        print("Line number: " + str(line_num))
        print("Instruction: " + line_text)
        self.parse_errors += 1

    def QCprintout(self):
        if self.website:
            print("Website: " + self.website)
        print("Number of instructions read: " + str(len(self.instructions)))
        print("Number of errors: " + str(self.parse_errors))
        if self.parse_errors > 0:
            print("Errors in parsing; Instructions probably not complete for web navigation.")
    
    def print(self):
        for i in range(len(self.instructions)):
            if i == self.current_idx:
                print(' '.join(self.instructions[i]) + '***')
            else:
                print(' '.join(self.instructions[i]))


    def setDelimiter(self,delimiter):
        self.delimiter=delimeter
        

if __name__=='__main__':
    instructions=navinput('demo.txt')
    instructions.setup()
    print(instructions.all())
