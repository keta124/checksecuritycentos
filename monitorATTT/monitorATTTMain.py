'''
Created on Dec 1, 2016

@author: sontn
'''
import checkSSHLogin
import checkPortOpen
import time
if __name__ == '__main__':
    try:
        while True:
            list_Login= checkSSHLogin.getListLogin()
            #list_Port_Change= checkPortOpen.getListPortOpen()
            time.sleep(10)
            print "OK"
    except:
        print "ERROR Except"
