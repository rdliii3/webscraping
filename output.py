import os, sys
import datetime

class Output():
    '''The output class controls the output for data gathering classes.'''

    def __init__(self, file=None, type="screen"):
        self.setOutputType(type)
        self.setFile(file)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.close()

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
            print("Could not open output file or not file given. Default output will be to screen\n")
    
    def outputType(self):
        return self.type

    def setOutputType(self,type):
        self.type=type

    def close(self):
        if self.fout:
            self.fout.close()

    def __del__(self):
        if self.fout:
            self.close()

if __name__=='__main__':
    test=Output()
    test_data=[['this','is','a','test'],['second','line']]
    test.csv(test_data)
    test.setFile("test.txt")
    test.setOutputType("csv")
    test.csv(test_data)
