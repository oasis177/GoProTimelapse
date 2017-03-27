#!/usr/bin/python

import commands
import urllib, requests
import time
import datetime
import os
import smtplib
import ftpBckup
import xml.etree.ElementTree as xml1
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from wifi import *
LogRute = '/home/pi/Desktop/goProPython/Logs/'

class GoPro:
    @staticmethod
    def EnviarMail(option):
        try:
            #Opcion 0 para Connexion perdida
            #Opcion 1 para foto no guardada
            config = xml1.parse('Config.xml').getroot()
            user = ""
            pwd = ""
            if (len(config.findall("frommail")) > 0):
                user = config.findall("frommail")[0].text
            if (len(config.findall("mailpwd")) > 0):
                pwd = config.findall("mailpwd")[0].text
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(user,pwd)
            msg = MIMEMultipart()
            msg['From'] = user
            for des in config.findall("destmail"):
                 msg['To'] = des.text
           
            if option == 0:
                  msg['Subject'] = "GoPro Connection LOST"
                  text = "Se ha perdido la connexion de la GoPro"
            elif option == 1:
                  msg['Subject'] = "GoPro couldn't save photo"
                  text = "No se ha guardado la ultima foto de la GoPro" 
            part1 = MIMEText(text,'plain')
            msg.attach(part1)
            for des in config.findall("destmail"):
                server.sendmail(user,des.text,msg.as_string())
            server.quit()
        except Exception,e:
            print(e)
            server.quit()
            pass
    @staticmethod
    def GetDir(option = 0):
    #OPTION 0 -> DECIDE POR EL DIR MAS ALTO
    #OPTION 1 -> USER ESCOJE EL DIR
       url = 'http://10.5.5.9:8080/DCIM/'
       lastImg = 0
       CurrDir = ''
       CurrNum = 0
       ListDirs = []
       try:
          resp = requests.get(url,timeout = 100)
          soup = BeautifulSoup(resp.content,'html5lib')    
          incr = 1
          for dirs in soup.findAll('a'):
              if 'GOPRO' in dirs.get('href') or 'gopro' in dirs.get('href'):
                try:
                   d1 = int(dirs.get('href')[0:dirs.get('href').index('GOPRO')])
                   if (option == 0):
                      if d1 > CurrNum:
                         CurrDir = dirs.get('href')
                         CurrNum = d1
                   elif (option == 1):
                      print("PULSA " + str(incr) +  ": " + str(dirs.get('href')))
                      ListDirs.append(dirs.get('href'))
                      incr += 1
                except Exception,e:
                   print e
                   pass
                   
          if (option == 1):
             while True:
                Inp = raw_input()
                if Inp.isdigit():
                   if (int(Inp)) > 0 and (int(Inp) -1) < len(ListDirs):
                      CurrDir = ListDirs[int(Inp) - 1]
                      break
                   else:
                      print("El valor introducido no es correcto, vuelve a introducirlo:")
                else:
                   print("El valor introducido no es correcto, vuelve a introducirlo:")

       except Exception, e:
          pass
       return(unicode(url + CurrDir))

    @staticmethod
    def LastPhoto():
        url = GoPro.GetDir(0)
        lastImg = 0
        try:
           resp = requests.get(url,timeout = 100)
           soup = BeautifulSoup(resp.content,'html5lib')
           for img in soup.findAll('a'):
               if '.JPG' in img.get('href') or '.jpg' in img.get('href'):
                 try:
                    numImg = int(img.get('href')[4:img.get('href').index('.')])
                    if numImg > lastImg:
                        lastImg = numImg
                 except Exception,e:
                    pass
                    #GoPro.EnviarMail(1)
                    #LogError = open(LogFile,'ab+')
                    #LogError.write("ERROR NO SAVED PHOTO: " + str(datetime.datetime.now()) + "\n")
                    #LogError.close()
           f1 = open(LogRute + 'LP.log','w')
           f1.write(str(lastImg))
           f1.close()
        except Exception, e:
           print e
           #GoPro.EnviarMail(1)
           #LogError = open(LogRute + 'LogGoPro.txt','ab+')
           #LogError.write("ERROR NO SAVED PHOTO: " + str(datetime.datetime.now()) + "\n")
           #LogError.close()
        
        return lastImg
                   
    def ComprovarBackup():
        try:     
            fdate = open(LogRute + 'lastbackup.txt','a+')
            str1 = fdate.readline().strip()
            if (str1 == ""):
                fdate.write(str(datetime.datetime.now())+ "\n")
                ftpBckup.ftpBckup.load()
                fdate.close()
            else:
                try:
                    date1 = datetime.datetime.strptime(str1,'%Y-%m-%d %H:%M:%S.%f')
                    dateDif = datetime.datetime.now() - date1
                    if (dateDif.seconds/3600) > 23:
                        fdate.close()
                        os.remove(LogRute + 'lastbackup.txt')
                        fdate1 = open(LogRute + 'lastbackup.txt','a+')
                        fdate1.write(str(datetime.datetime.now())+ "\n")
                        ftpBckup.ftpBckup.load()
                        fdate1.close()          
                    else:
                        fdate.close() 
               
                except Exception,e:
                    print e
        except Exception:
            pass

    @staticmethod
    def start():
        Err = 0
        while(True):
            try:
                print("ENTRA")
                config = xml1.parse('Config.xml').getroot()
                wifiPwd = ""
                if (config.findall("wifipwd") != []):
                    wifiPwd = config.findall("wifipwd")[0].text
                curr = datetime.datetime.now().time()
                #GoPro.ComprovarBackup()
                f1 = open(LogRute + 'LP.log','r')
                numimg = int(f1.readline().strip())
                f1.close()
                if (curr.hour >= 6) and (curr.hour < 20):        
                    page = urllib.urlopen("http://10.5.5.9/bacpac/PW?t=" + wifiPwd + "&p=%01")
                    time.sleep(05)
                    page = urllib.urlopen("http://10.5.5.9/camera/CM?t=" + wifiPwd + "&p=%01")
                    time.sleep(05)
                    page = urllib.urlopen("http://10.5.5.9/bacpac/SH?t=" + wifiPwd + "&p=%01")
                    time.sleep(05)
                    #today = datetime.datetime.now()
                    #print("PENULTIMA IMG->" + str(numimg))
                    numimg1 = GoPro.LastPhoto()
                    #print("ULTIMA IMg->" + str(numimg1))
                    if page.code != 200 or (numimg + 1 != numimg1 and numimg1 != 0):
                        GoPro.EnviarMail(1)
                        LogError = open(LogRute + 'LogGoPro.txt','ab+')
                        LogError.write("ERROR NO SAVED PHOTO: " + str(datetime.datetime.now()) + "\n")
                        LogError.close()
                    else:
                        Err = 0
                        LogError = open(LogRute + 'LogGoPro.txt','ab+')
                        LogError.write("Saved photo "+ str(numimg1) + ": " + str(datetime.datetime.now()) + "\n")
                        LogError.close()
                time.sleep(1500)
            except KeyboardInterrupt:
                break
            except IOError:
                Err += 1
                if (Err == 1):           
                    GoPro.EnviarMail(0)
                    os.system("sudo ifconfig wlan0 down")
                    time.sleep(2)
                    os.system("sudo ifconfig wlan0 up")
                    LogError = open(LogRute + 'LogGoPro.txt','ab+')
                    LogError.write("Error: " + str(datetime.datetime.now()) + "\n")
                    LogError.write("Mail sent & Reset wlan: " + str(datetime.datetime.now()) + "\n")
                    LogError.close()
                elif Err > 1 and Err < 8:
                    os.system("sudo ifconfig wlan0 down")
                    time.sleep(2)
                    os.system("sudo ifconfig wlan0 up")
                    LogError = open(LogRute + 'LogGoPro.txt','ab+')
                    LogError.write("Reset wlan: " + str(datetime.datetime.now()) + "\n")
                    LogError.close()
                elif Err >= 8:
                    LogError = open(LogRute + 'LogGoPro.txt','ab+')
                    LogError.write("Reset Raspberry: " + str(datetime.datetime.now()) + "\n")
                    LogError.close()
                    os.system("sudo shutdown -r now")
                #TEST = Scheme.find('wlan0','NIL')
                #TEST.activate()     
                time.sleep(500)
        

    
