#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/13 上午10:35
# @Author  : Aries
# @Site    : 
# @File    : webdriver_process.py
# @Software: PyCharm Community Edition
import logging
from selenium import webdriver
from selenium.webdriver.support.select import Select
logger = logging.info(__name__)


class MethodNotFound(Exception):
    pass


class WebdriverProcess(object):

    def __init__(self, browser='ie'):
        if browser.lower() == 'ie':
            self.driver = webdriver.Ie()
        elif browser.lower() == 'chrome':
            self.driver = webdriver.Chrome()
        self.window_handle = []

    def action_navigate(self, url):
        self.driver.get(url)

    def action_clear_edit(self, webelement):
        webelement.clear()

    def send_keys(self, value, content, method):
        pass

    def execute_script(self, js):
        self.driver.execute_script(js)

    def method_unknow(self, value):
        raise MethodNotFound('%s不正确，请检查是否正确' % value)

    def select_values(self, s, method, value):
        select_method = 'select_by_' + s
        func = getattr(Select(s), select_method, self.method_unknow)
        func(value)

    def switch_to_new_windows(self, url):
        js_val = url
        js = 'window.open("%s");' % js_val
        self.execute_script(js)
        self.window_handle.append(self.driver.current_window_handle)
        handles = self.driver.window_handles
        for handle in handles:  # 切换窗口
            if handle != self.driver.current_window_handle:
                logger.info('switch to ', handle)
                self.driver.switch_to_window(handle)
                self.window_handle.append(self.driver.current_window_handle)
                break

    def input(self, method, method2, val):

        find = 'find_element_by_' + method
        func = getattr(self.driver, find, self.method_unknow)
        s = func()

        if method2 == 'clear':
            s.clear()
        else:
            s.send_keys(val)

    def quit(self):
        self.driver.quit()

    def navigate_url(self, url):
        self.driver.get(url)


if __name__ == '__main__':
    wp = WebdriverProcess('chrome')
    wp.navigate_url('http://cloud.tencent.com')
