'''
Created on Dec 1, 2016

@author: sontn
'''
import checkSSHLogin
import checkPortOpen
if __name__ == '__main__':
    try:
        List_Login= checkSSHLogin.getListLogin()
        checkPortOpen.getListPortOpen()
    except:
        print "ERROR Except"
