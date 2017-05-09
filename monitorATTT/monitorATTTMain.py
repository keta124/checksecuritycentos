'''
Created on Dec 1, 2016

@author: sontn
'''
import checkSSHLogin
import checkPortOpen
if __name__ == '__main__':
    try:
        list_Login= checkSSHLogin.getListLogin()
        list_Port_Change= checkPortOpen.getListPortOpen()
    except:
        print "ERROR Except"
