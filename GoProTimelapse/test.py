# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime

#OPTION 0 -> DECIDE POR EL DIR MAS ALTO
#OPTION 1 -> USER ESCOJE EL DIR
def GetDir(option = 0):
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
               #EnviarMail(1)
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
      
   
