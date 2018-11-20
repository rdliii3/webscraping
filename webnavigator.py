from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website import website
from webparser import webparser
from navinput import navinput
from output import Output
import os,sys


class webnavigator():
    '''The webnavigator class will read from a file a series of steps to take when interacting with a website. Each line of the file will contain an element identifier, type of element identifier,action, and optional action control string. Allowable actions for the input string are click,send_keys,find_element_by_id,find_element_by_name,find_element_by_xpath.'''

    def __init__(self,filePath):
        # Setup program variables
        self.config()
        # Initialize instruction object
        self.instructions = navinput(filePath)
        self.instructions.setup()
        # Initialize website object
        self.website = website(self.instructions.website)
        # Initialize webdriver
        self.driver = webdriver.Firefox(executable_path = self.config_params['driver'])
        self.driver.get(self.website.url)
        # Initialize output object
        self.output = None
        # Initialize data objects
        self.dataList = []
        self.url_stack=[] # created for step back ability


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
    
    def config(self):
        #default configuration
        self.config_params = {"driver_type":"Firefox", "driver":os.getenv('HOME')+'/geckodriver'} 
        # Read configuration from file if possible
        if not os.path.isfile(os.getenv('HOME')+'/.web/.config'):
            return
        with open(os.getenv('HOME')+'/.web/.config','r') as config:
            #build configuration dictionary
            for line in config.readlines():
                if line[0] == '': #skip empty lines
                    continue
                if line[0] == '#': #skip comment lines
                    continue
                self.config_params[ line.split('=')[0].strip() ]= line.split('=')[1].strip()


    def execute(self,instruction):
        '''This function takes an instruction and executes it
        Input - An instruction (list of 4 items)
        Return - True for success, False for error
        '''
        try:

            element_id,element_type,action,string = instruction

            #get element
            if element_type=='id':
                element = self.driver.find_element_by_id(element_id)
            elif element_type=='name':
                element = self.driver.find_element_by_name(element_id)
            elif element_type=='xpath':
                element = self.driver.find_element_by_xpath(element_id)
            #perform action
            if action=='click':
                element.click()
            elif action=='send_keys':
                if string=='username':
                    element.send_keys(website.username())
                elif string=='password':
                    element.send_keys(website.password())
                else:
                    element.send_keys(string)
            elif action=='parse':
                self.parse(element.get_attribute('outerHTML'),string)
            elif action=='output':
                self.write()
            elif action=='flush':
                self.flush()
            return True
        except:
            self.instructionError()
            return False
            
    def executeByStep(self):
        '''Function to control execution by step from the user'''
        instruction = self.instructions.current()
        while instruction:
            self.url_stack.append(self.driver.current_url)
            user_response = input("Press N for next, B for back, C for custom, P for print: ")
            if user_response.isdigit():
                instruction = self.instructions.byIndex(int(user_response))
                user_response = 'n'
            if user_response.lower() == 'n':
                print(instruction)
                if self.execute(instruction):
                    instruction=self.instructions.next()
            elif user_response.lower() == 'b':
                self.url_stack.removeAll(self.driver.current_url)
                self.driver.get(self.url_stack.pop())
                print(self.url_stack)
                instruction=self.instructions.previous()                
            elif user_response.lower() == 'c':
                custom = input("Enter new instruction to insert: ")
                self.instructions.insert(custom)
            elif user_response.lower() == 'p':
                self.instructions.print()
            elif user_response.lower() == 'q':
                return

        self.instructions.last()
        self.executeByStep() # Loop back into execution steps so user can step back from last instruction if needed
                


    def executeAll(self):
        '''Function to execute all instructions in an instruction set'''
        instruction = self.instructions.current()
        while instruction:
            if not self.execute(instruction):
                break
            instruction = self.instructions.next()

    def parse(self,html,parse_type):
        '''Function to parse html data in a user defined way
        Input: html - html to be parsed
               parse_type - parameter that controls how the html will be parsed
        Return: N/A
        Side effect: Fill dataList with parsed html
        '''
        parser = webparser(html,parse_type)
        self.dataList += parser.parse()

    def data(self):
        '''This function provides access to the data obtained from scraping
        Input - None
        Return - list of strings
        Side effect - None
        '''
        return self.dataList

    def flush(self):
        self.dataList.clear()

    def setOutput(self, outputObject):
        if isinstance(outputObject, Output):
            self.output = outputObject

    def write(self):
        if self.output:
            self.output.write(self.dataList)
        else:
            print(self.dataList)
            
    def close(self):
        self.driver.close()
    
    def instructionError(self):
        print("Could not execute instruction:")
        print(self.instructions.current())


        
if __name__=='__main__':
    # default arguments
    instructionFile = 'demo.txt'
    OutputObj = None
    outputType = None
    execute = 'all'

    # get user arguments
    if '-s' in sys.argv:
        sys.argv.remove('-s')
        execute = 'step'
    if len(sys.argv) > 1:
        instructionFile = sys.argv[1]
    if len(sys.argv) > 2:
        outputType = sys.argv[2].split('.')[1]
        OutputObj = Output(sys.argv[2], outputType)

    with webnavigator(instructionFile) as navigator:
        navigator.setOutput(OutputObj)
        if execute == 'step':
            navigator.executeByStep()
        else:
            navigator.executeAll()
            






                
        
