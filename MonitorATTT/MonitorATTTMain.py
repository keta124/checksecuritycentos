'''
Created on Dec 1, 2016

@author: sontn
'''
import CheckSSHLogin
import CheckPortOpen
if __name__ == '__main__':
    try:
        List_Login= CheckSSHLogin.GetListLogin()
        CheckPortOpen.GetListPortOpen()
    except:
        print "ERROR Except"