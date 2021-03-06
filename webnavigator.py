from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from website import website
from webparser import webparser
from navinput import navinput
from output import Output
import os, sys
from time import sleep


class webnavigator():
    '''The webnavigator class will read from a file a series of steps to take when interacting with a website. Each line of the file will contain an element identifier, type of element identifier,action, and optional action control string. Allowable actions for the input string are click,send_keys,find_element_by_id,find_element_by_name,find_element_by_xpath.'''

    def __init__(self,filePath, log=False):
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
        # Set object attributes
        self.log=log
        self.attempts = 0

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
        if self.log:
            print('Executing: ' + ' '.join(instruction))
        

        element_id,element_type,action,string = instruction

        try:
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
            elif action=='select':
                if string.isdigit():
                    Select(element).select_by_index(string)
                else:
                    try:
                        Select(element).select_by_visible_text(string)
                    except:
                        Select(element).select_by_value(string)
            elif action=='send_keys':
                if string=='username':
                    element.send_keys(self.website.username())
                elif string=='password':
                    element.send_keys(self.website.password())
                elif string=='prompt':
                    self.website.prompt()
                else:
                    element.send_keys(string)
            elif action=='parse':
                self.parse(element.get_attribute('outerHTML'),string)
            elif action=='output':
                self.write(string)
            elif action=='flush':
                self.flush()
            elif action=='pause':
                sleep(int(string))
            self.attempts = 0
            return True

        except Exception as e:
            # Try to execute instruction 3 times before failing
            if self.attempts < 3:
                self.attempts += 1
                sleep(self.attempts)
                return self.execute(instruction)
            else:
                self.instructionError(e)
                return False
            
    def executeByStep(self):
        '''Function to control execution by step from the user'''
        instruction = self.instructions.current()
        self.url_stack.append(self.driver.current_url)
        while instruction:
            user_response = input("Enter step option(n=next, b=back, q=quit, m=more info): ")
            if user_response.isdigit():
                instruction = self.instructions.byIndex(int(user_response))
                user_response = 'n'
            if user_response.lower() == 'n':
                if self.execute(instruction):
                    instruction=self.instructions.next()
                    self.url_stack.append(self.driver.current_url)
            elif user_response.lower() == 'b':
                if self.url_stack:
                    self.driver.get(self.url_stack.pop())
                print(self.url_stack)
                instruction=self.instructions.previous()                
            elif user_response.lower() == 'i':
                custom = input("Enter new instruction to insert: ")
                self.instructions.insert(custom)
            elif user_response.lower() == 'p':
                self.instructions.print()
            elif user_response.lower() == 'c':
                return self.executeAll()
            elif user_response.lower() == 'm':
                self.printStepOptions()
            elif user_response.lower() == 'q':
                return

        self.instructions.last()
        return self.executeByStep() # Loop back into execution steps so user can step back from last instruction if needed
                


    def executeAll(self):
        '''Function to execute all instructions in an instruction set'''
        instruction = self.instructions.current()
        while instruction:
            if not self.execute(instruction):
                user = input("Continue in step-by-step mode?(y/n): ")
                if user.lower() == 'y':
                    self.executeByStep()
                else:
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

    def printStepOptions(self):
        print('''
        Below are all the available options for step-by-step mode.
        Input can be entered as either upper or lower case.
        Entering a number will execute that indexed instruction.
        
        N: next instruction
        B: back one instruction (but does not execute);
           also steps back in the URL stack. Note that going
           forward and backwards can result in a disconnect between the
           instructions and URLs. Using an instruction index execute the 
           appropriate instruction for the current URL.
        P: print all instructions; current instruction (will be executed on
           'N' input) is denoted with '***'
        Q: Quit execution
        I: insert a custom instruction; this inserts a custom user instruction
           after the current instruction. Currently this only affects instructions
           as held in memory.
        C: continue until an exception occurs or all instructions complete
        M: List all options
        [0-9]+: Execute instruction at numbered index
        ''')

    def flush(self):
        self.dataList.clear()

    def setOutput(self, outputObject):
        if isinstance(outputObject, Output):
            self.output = outputObject
        else:
            self.output = None

    def write(self, outputFile=None):
        if outputFile:
            # new output file given
            if self.output:
                self.output.close()
            self.output = Output(outputFile, outputFile.split('.')[1])
            self.output.write(self.dataList)
        else:
            # Single file (or screen) output case
            self.output.write(self.dataList)
        
            
    def close(self):
        self.driver.close()
    
    def instructionError(self, exception):
        print("Could not execute instruction:")
        print(self.instructions.current())
        print(repr(exception))


        
if __name__=='__main__':
    # default arguments
    instructionFile = 'demo.txt'
    OutputObj = None
    outputType = None
    execute = 'all'
    log = False

    # parse user arguments
    if '-s' in sys.argv:
        sys.argv.remove('-s')
        execute = 'step'
    if '-l' in sys.argv:
        sys.argv.remove('-l')
        log=True
    if len(sys.argv) > 1:
        instructionFile = sys.argv[1]
    if len(sys.argv) > 2:
        outputType = sys.argv[2].split('.')[1]
        OutputObj = Output(sys.argv[2], outputType)
    else:
        OutputObj = Output()

    # Run
    with webnavigator(instructionFile, log) as navigator:
        navigator.setOutput(OutputObj)
        if execute == 'step':
            navigator.executeByStep()
        else:
            navigator.executeAll()
            






                
        
