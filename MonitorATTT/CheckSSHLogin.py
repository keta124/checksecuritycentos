'''
Created on Jan 6, 2017

@author: sontn
'''
import os, sys
import datetime
def writefile(file_write_,content):
    try:
        path =os.path.abspath(os.path.dirname(sys.argv[0]))
        statinfo = os.stat(path)
        ## 
        if str(file_write_) == "Output/tmp_check_login_duplicate.log":
            file_write = path+"/"+str(file_write_)
            f = open(file_write,"wb")
            f.close()
            os.chown(file_write, statinfo.st_uid, statinfo.st_gid)
            f = open(file_write,"wb")
            f.write(content)
            f.close()
        else :
            file_write = path+"/"+str(file_write_)
            f = open(file_write,"ab")
            f.close()
            os.chown(file_write, statinfo.st_uid, statinfo.st_gid)
            f = open(file_write,"ab")
            f.write(content)
            f.close()
    except:
        print "Except writefile"

def compare_duplicate(file_write_,content):
    try:
        path =os.path.abspath(os.path.dirname(sys.argv[0]))
        file_write = path+"/"+str(file_write_)
        f = open(file_write,"r+")
        lines = f.read()
        if lines == content:    
            return True
        else:
            return False
    except:
        return False

def is_valid_ip(address):
    try:
        parts = address.split(".")
        if len(parts) != 4:
            return "0.0.0.0"
        for item in parts:
            if not 0 <= int(item) <= 255:
                return "0.0.0.0"
        return address
    except:
        return "0.0.0.0"
    
def GetListLogin():
    try:
        output= str(os.popen("last | grep still|grep pts|sed -n 's/ \+/ /gp'|cut -d ' ' -f1-7").read())
        hostname_ip = str(os.popen("hostname -I").read()).replace(" \n","").replace(" ","||")
        list_output=output[:-1].split('\n')
        list_login=[]
        list_check_duplicate=[]
        for element in list_output:
            a = element.split(' ')
            # Make json output
            json_login="{"
            list_check_duplicate_=[]
            login_time = ""+a[3]+" "+a[4]+" "+a[5]+" "+a[6]+ " "+datetime.datetime.now().strftime("%Y")
            login_time_ = datetime.datetime.strptime(login_time, "%a %b %d %H:%M %Y").strftime("%Y-%m-%dT%H:%M:%S.%f+0700")
            ip_login = is_valid_ip(address=str(a[2]))
            json_login= json_login+'"time_stamp":"'+str(login_time_)+'","username":"'+str(a[0])+'","src_ip":"'+ip_login+'","dest_ip":"'+hostname_ip+'"}'
            #### remove time check duplicate 
            list_check_duplicate_.append(str(a[0]))
            list_check_duplicate_.append(ip_login)
            if list_check_duplicate_ not in list_check_duplicate:
                list_check_duplicate.append(list_check_duplicate_)
                list_login.append(str(json_login))
        check_duplicate= compare_duplicate("Output/tmp_check_login_duplicate.log",str(list_check_duplicate))
        if not check_duplicate:
            writefile("Output/tmp_check_login_duplicate.log",str(list_check_duplicate))
            login_write = "\n".join(list_login)+"\n"
            writefile("Output/ATTT_login_ssh.log",login_write)
        return list_login
    except:
        return []
