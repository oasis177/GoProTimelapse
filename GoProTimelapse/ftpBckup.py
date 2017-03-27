from ftplib import FTP

class ftpBckup(object):
    
    def __init__(self,params):
        '''Constructor'''

    @staticmethod
    def load():        
        try:
            ftp = FTP('192.168.100.50')
            ftp.login('oscar.d','Osim2000')
            ftp.cwd('/servidorsql/Programas visual/Python/goPro')
            ftp.storlines('STOR goPro.py',open('goPro.py','r'))
            ftp.storlines('STOR LogGoPro.txt',open('LogGoPro.txt','r'))
            ftp.close()
            return "FTP CORRECTO"
        except Exception,e:
            print e
    
