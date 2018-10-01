from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website import website
from webparser import webparser
from navinput import navinput
import os,sys


class webnavigator():
    '''The webnavigator class will read from a file a series of steps to take when interacting with a website. Each line of the file will contain an element identifier, type of element identifier,action, and optional action control string. Allowable actions for the input string are click,send_keys,find_element_by_id,find_element_by_name,find_element_by_xpath.'''

    def __init__(self,filePath):
        #setup internal objects/attributes
        self.config()
        self.instructions=navinput(filePath)
        self.instructions.setup()
        self.website=website(self.instructions.website)
        self.driver=webdriver.Firefox(executable_path=self.config_params['driver'])

    
    def config(self):
        self.config_params={}
        with open(os.getenv('HOME')+'/.web/.config','r') as config:
            #build configuration dictionary
            for line in config.readlines():
                if line[0] == '': #skip empty lines
                    continue
                if line[0] == '#': #skip comment lines
                    continue
                self.config_params[ line.split('=')[0].strip() ]= line.split('=')[1].strip()


    def execute(self):
        '''This function takes the instructions and executes them one by one'''
        self.driver.get(self.website.url)

        instruction=self.instructions.current()
        while instruction:
            element_id,element_type,action,string=instruction

            if element_type=='id':
                element=self.driver.find_element_by_id(element_id)
            elif element_type=='name':
                element=self.driver.find_element_by_name(element_id)
            elif element_type=='xpath':
                element=self.driver.find_element_by_xpath(element_id)
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
            
            instruction=self.instructions.next()
        self.driver.close()

    def parse(self,html,parse_type):
        parser=webparser(html,parse_type)
        self.dataList=parser.parse()

    def data(self):
        '''This function provides access to the data obtained from scraping
        Input - None
        Return - list of strings
        Side effect - None
        '''
        return self.dataList

        
        
if __name__=='__main__':
    navigator=webnavigator('demo.txt')
    navigator.execute()
    print(navigator.data())


                
        
