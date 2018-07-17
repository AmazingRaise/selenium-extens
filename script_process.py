 #!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 上午10:10
# @Author  : Aries
# @Site    : 
# @File    : webdriver_process.py.py
# @Software: PyCharm Community Edition
import logging
import time

from .excel_helper import ExcelReader
from .webdriver_process import WebdriverProcess

logger = logging.getLogger(__name__)


class ScriptProcess(object):

    def __init__(self, filename, browser_name='ie'):
        self.file_name = filename
        self.scripts_content = None
        self.webdriver = WebdriverProcess(browser_name)

    def start(self):
        self.get_scripts_list()
        self.deal_scripts_list()

    def get_scripts_list(self):
        er = ExcelReader()
        self.scripts_content = er.start(self.file_name)

    def deal_scripts_list(self):
        for content in self.scripts_content:
            self.action_one_cmd(content)

    def action_one_cmd(self, content):

        if content[0] == 'click':
            method = 'find_element_by_' + content[1]
            val = content[3]
            self.method_find(method, val).click()

        elif content[0] == 'find':
            method = 'find_element_by_' + content[1]
            val = content[3]
            self.method_find(method, val)

        elif content[0] == 'select':
            method = content[1]
            select_method = content[2]
            element_val = content[3]
            select_val = content[4]
            s = self.method_find(method, element_val)
            self.webdriver.select_values(s, select_method, select_val)

        elif content[0] == 'switch_to_new_window':
            self.webdriver.switch_to_new_windows(content[3])

        elif content[0] == 'init_url':
            val = content[3]
            self.webdriver.navigate_url(val)

        elif content[0] == 'excute_js':
            js = content[3]
            self.webdriver.execute_script(js)
        elif content[0] == 'input':
            self.webdriver.input(method=content[1],
                                 method2=content[2],
                                 val=content[3])
        elif content[0] == 'sleep':
            time.sleep(int(content[3]))
        else:
            logger.info('方法名未知， 请核对后继续')

    def quit(self):
        self.webdriver.quit()

    def method_find(self, method, val):
        func = getattr(self.webdriver.driver, method, self.webdriver.method_unknow)
        return func(val)


if __name__ == '__main__':
    sp = ScriptProcess('new_script.xlsx', browser_name='chrome')
    sp.start()
    sp.quit()
