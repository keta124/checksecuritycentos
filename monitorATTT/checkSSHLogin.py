'''
Created on Jan 6, 2017

@author: sontn
'''
import os, sys
import datetime
def writefile(file_write_,content):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
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

def compare_duplicate(file_write_,content): # content list => return list
    try:
        # compare and write newfile
        path =os.path.abspath(os.path.dirname(sys.argv[0]))
        file_write = path+"/"+str(file_write_)
        f = open(file_write,"r+")
        list_content = []
        lines = f.readlines()
        for content_ in content:
            content_add = content_ +"\n"
            if content_add not in lines:
                list_content.append(content_)
        f.close()
        return list_content
    except:
        return []

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
    
def getListLogin():
    try:
        output= str(os.popen("last | grep still|grep pts|sed -n 's/ \+/ /gp'|cut -d ' ' -f1-7").read())
        hostname_ip = str(os.popen("hostname -I").read()).replace(" \n","").replace(" ","||")
        list_output=output[:-1].split('\n')  # convert to list
        list_login=[] # new login session
        list_new_login= compare_duplicate("Output/tmp_check_login_duplicate.log",list_output)
        login_tmp_write = "\n".join(list_output)+"\n"
        writefile("Output/tmp_check_login_duplicate.log",str(login_tmp_write))
        if len(list_new_login)>0:
            for element in list_new_login:
                a = element.split(' ')
                # Make json output
                json_login="{"
                login_time = ""+str(a[3])+" "+str(a[4])+" "+str(a[5])+" "+str(a[6])+ " "+datetime.datetime.now().strftime("%Y")
                login_time_ = datetime.datetime.strptime(login_time, "%a %b %d %H:%M %Y").strftime("%Y-%m-%dT%H:%M:%S.%f+0700")
                ip_login = is_valid_ip(address=str(a[2]))
                json_login= json_login+'"time_stamp":"'+str(login_time_)+'","username":"'+str(a[0])+'","src_ip":"'+ip_login+'","dest_ip":"'+hostname_ip+'"}'
                list_login.append(str(json_login))
            login_write = "\n".join(list_login)+"\n"
            writefile("Output/ATTT_login_ssh.log",login_write)
            return list_login
    except:
        return []
