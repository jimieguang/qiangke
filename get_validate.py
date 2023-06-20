#coding=utf-8
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import FirefoxOptions
import numpy as np

from io import BytesIO
import time, requests
import re
# from webdriver_manager.chrome import ChromeDriverManager

import os
import random

# 引入自定义函数用于判断滑动距离
from find import *

class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，破解滑动验证码
    """
    def __init__(self):
        self.url = "file:///"+os.getcwd()+'/code.html'
        # 声明一个谷歌配置对象
        self.opts = FirefoxOptions()
        self.opts.set_headless() 

        self.driver = webdriver.Firefox(log_path=r'./webdriver.log',firefox_options=self.opts)
        self.wait = WebDriverWait(self.driver, 20)
        # 伪造浏览器指纹，防止被检测出(参考资料：https://jishuin.proginn.com/p/763bfbd33b73)
        with open('./stealth.min.js') as f:
            js = f.read()
        self.driver.execute_script(js)

    def open(self):
        self.driver.get(self.url)
        
    def refresh(self):
        # 刷新当前界面
        self.driver.refresh()
    
    def stop(self):
        # 关闭浏览器，停止程序
        self.driver.close()
        
    def get_pic(self):
        # 注释掉了无意义的图片获取（即template）
        # 加入了对获取空url（None）的处理
        time.sleep(0.5)
        target = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        target_link = target.get_attribute('src')
        while target_link==None:
            time.sleep(0.5)
            target_link = target.get_attribute('src')
        # print(target_link)
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        target_img.save('./temp/target.jpg')

    def get_tracks(self, distance, ease_func):
        seconds = random.randint(2, 4)
        distance += 20
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = ease_func
            offset = round(ease(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
        return tracks
    
    def ease_out_quart(self,x):
        return 1 - pow(1 - x, 4)


    def crack_slider(self,distance):
        distance = distance+8
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_slider')))
        trackes = self.get_tracks(distance,self.ease_out_quart)
        ytrackes = self.get_tracks(20,self.ease_out_quart)
        
        ActionChains(self.driver).click_and_hold(slider).perform()
        while trackes:
            x = trackes.pop(0)
            if ytrackes!=[]:
                y = ytrackes.pop(0)
            else:
                y = random.randint(2, 4)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=y).perform()
            time.sleep(0.02)
        time.sleep(0.05)
        # ActionChains(self.driver).move_by_offset(xoffset=distance, yoffset=0).perform()
        ActionChains(self.driver).release().perform()
        validate_element = self.driver.find_element_by_id('validate')
        time.sleep(0.5)
        validate = validate_element.get_attribute('outerHTML')
        validate = re.findall(re.compile('>(.*?)</div'),validate)[0]
        return validate




def get_validate():
    cs = CrackSlider()
    cs.open()
    print("waiting")
    # 等待第一张图片出现
    cs.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
    print("初始化完毕")
    while True:
        cs.get_pic()
        # 比对五个已知图片，用于确定缺口图片为哪副
        for i in range(1,6):
            fileorder = find_pic(i)
            if fileorder != 0:
                break
        distance = find_distance(fileorder)
        if distance != 0:
            validate = cs.crack_slider(distance)
        if validate!= "":
            cs.stop()
            return validate
        # cs.refresh()

if __name__ == '__main__':
    import threading
    class myThread (threading.Thread):   #继承父类threading.Thread
        """多线程类"""
        def __init__(self, threadID, function_name,list):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.func = function_name
            self.list = list
        def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
            print("Starting " + self.threadID)
            self.func()
    validate_list = ["running"]
    thread1 = myThread("1", get_validate, validate_list)
    thread1.start()
    input("停止请键入enter:")
    validate_list[0] = "end"
