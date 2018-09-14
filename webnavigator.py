from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from website import website
from webparser import webparser
import os,sys


class webnavigator():
    '''The webnavigator class will read from a file a series of steps to take when interacting with a website. Each line of the file will contain an element name, type of element identifier,action, and optional input string. Allowable actions for the input string are click,send_keys,find_element_by_id,find_element_by_name,find_element_by_xpath.'''

    def __init__(self,filePath,url):
        #setup internal objects/attributes
        self.inFile=filePath
        self.website=website(url)
        self.driver=webdriver.Firefox(executable_path=r'/home/rlangley/geckodriver')
        self.instructions=[]
        #get instructions from file
        with open(self.inFile,'r') as fd:
            self.instructions=fd.readlines()


    def execute(self):
        '''This function takes the instructions and executes them one by one'''
        self.driver.get(self.website.url)
        for line in self.instructions:
            element_id,element_type,action,string=line.split('\t')
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

    def parse(self,html,parse_type):
        webparser(html,parse_type)
        self.data=webparser.text()
        
        
if __name__=='__main__':
    navigator=webnavigator('demo.txt','www.fftoday.com')
    navigator.execute()


                
        
