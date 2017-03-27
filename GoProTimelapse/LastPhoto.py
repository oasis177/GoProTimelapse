import commands
import urllib, requests
import time
import datetime
import os

import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from wifi import *

def LastPhoto():
    url = 'http://10.5.5.9:8080/DCIM/105GOPRO/'
    lastImg = 0
    try:
       resp = requests.get(url,timeout = 60)
       soup = BeautifulSoup(resp.content,'html5lib')    
       for img in soup.findAll('a'):
           if '.JPG' in img.get('href') or '.jpg' in img.get('href'):
             try:
                numImg = int(img.get('href')[4:img.get('href').index('.')])
                if numImg > lastImg:
                    lastImg = numImg
             except Exception,e:
                LogError = open('Logs/LogGoPro.txt','ab+')
                LogError.write("ERROR NO SAVED PHOTO: " + str(datetime.datetime.now()) + "\n")
                LogError.close()
 
    except Exception, e:
        LogError = open('Logs/LogGoPro.txt','ab+')
        LogError.write("ERROR NO SAVED PHOTO: " + str(datetime.datetime.now()) + "\n")
        LogError.close() 
    return lastImg

def GetPreLastImg():
    f1 = open(
