import os, sys
import datetime

class Output():
    '''The output class controls the output options data gathering classes.'''

    def __init__(self, file=None, type="screen"):
        self.setOutputType(type)
        self.setFile(file)

    def csv(self, data):
        # Create csv string for output
        intermediate_data=[]
        out_string = '\n### ' + str(datetime.datetime.now()) + ' ###\n'
        for line in data:
            if isinstance(line, list):
                intermediate_data.append(','.join(line))
        out_string += '\n'.join(intermediate_data)
        # Output
        return out_string
        
    def txt(self, data):
        # Create txt string for output
        intermediate_data=[]
        out_string = '\n### ' + str(datetime.datetime.now()) + ' ###\n'
        for line in data:
            if isinstance(line, list):
                intermediate_data.append(' '.join(line))
        out_string += '\n'.join(intermediate_data)
        # Output
        return out_string


    def write(self, data):
        if self.fout:
            if self.type == 'csv':
                self.fout.write(self.csv(data))
            if self.type == 'txt':
                self.fout.write(self.txt(data))
        else:
            print(self.csv(data))

    def file_handle(self):
        return self.fout

    def setFile(self, file):
        self.file=file
        if self.file:
            self.fout=open(self.file,'w')
        else:
            self.fout=None
            print("Could not open output file. Default output will be to screen\n")
    
    def outputType(self):
        return self.type

    def setOutputType(self,type):
        self.type=type


if __name__=='__main__':
    test=Output()
    test_data=[['this','is','a','test'],['second','line']]
    test.csv(test_data)
    test.setFile("test.txt")
    test.setOutputType("csv")
    test.csv(test_data)
