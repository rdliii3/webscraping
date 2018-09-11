from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import website
import os

class webnavigator():
    '''The webnavigator class will read from a file a series of steps to take when interacting with a website. Each line of the file will contain an element name, type of element identifier,action, and optional input string. Allowable actions for the input string are click,send_keys,find_element_by_id,find_element_by_name,find_element_by_xpath.'''

    def __init__(self,filePath=None,url=None):
        #setup internal objects/attributes
        self.inFile=filePath
        self.website=website(url)
        self.driver=webdriver.Firefox()
        self.instructions=[]
        #get instructions if file
        with open(self.inFile,'r') as fd:
            self.instructions=fd.readlines()

    def execute():
        '''This function takes the instructions and executes them one by one'''
        self.driver.get(website.url)
        for line in self.instructions:
            element_id,element_type,action,string=line.split(',')
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
                if string='username':
                    element.send_keys(website.username())
                elif string=='password':
                    element.send_keys(website.password())
                else:
                    element.send_keys(string)
            elif action=='parse':
                self.parse(element.get_attribute('outerHTML'),string)

    def parse(html,parse_type):
        self.data+=webparser(html,parse_type)
        self.data+='\n'




                
        
