'''
Created on Jan 6, 2017

@author: sontn
'''
import os,sys
import datetime

def writefile(file_write_,content):
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        statinfo = os.stat(path)
        ## 
        if str(file_write_) == "Output/tmp_check_port_duplicate.log":
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

def read_tmp_file():
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        file_tmp = path+"/"+"Output/tmp_check_port_duplicate.log"
        f = open(file_tmp,"r+")
        lines = f.read()
        return lines
    except:
        return ""

def getListPortOpen():
    try:
        hostname_ip = str(os.popen("hostname -I").read()).replace(" \n","").replace(" ","||")
        ## Get current port open
        output_tcp= str(os.popen("netstat -ntl|awk '{print $4}'|awk '!/127.0.0.1/ && !/::1:/ && !/Local/ && !/only/ ' | awk -F ':' '{print $NF}' |sort -n |uniq ").read())
        output_udp= str(os.popen("netstat -nul|awk '{print $4}'|awk '!/127.0.0.1/ && !/::1:/ && !/Local/ && !/only/ ' | awk -F ':' '{print $NF}' |sort -n |uniq ").read())
        list_output_tcp=output_tcp[:-1].split('\n')
        list_output_udp=output_udp[:-1].split('\n')
        #print list_output_tcp
        #print list_output_udp
        # Compare with port save in file
        list_output_all = str(list_output_tcp)+"\n"+str(list_output_udp)
        list_check_duplicate=[]
        list_check_duplicate.append(list_output_tcp)
        list_check_duplicate.append(list_output_udp)
        
        ## Check duplicate
        lines = read_tmp_file()
        if lines != list_output_all:
            writefile("Output/tmp_check_port_duplicate.log",list_output_all)
            list_tcp_open=[]
            list_tcp_close=[]
            list_udp_open=[]
            list_udp_close=[]
            list_lines=lines.split('\n')
            list_tcp_tmp = list_lines[0].replace('[','').replace(']','').replace("'","").split(', ')
            list_udp_tmp = list_lines[1].replace('[','').replace(']','').replace("'","").split(', ')
            # check open or close port
            # tcp
            for tcp in list_tcp_tmp:
                if tcp not in list_output_tcp:
                    list_tcp_close.append(tcp)
            for tcp_ in list_output_tcp:
                if tcp_ not in list_tcp_tmp:
                    list_tcp_open.append(tcp_)
            # udp
            for udp in list_udp_tmp:
                if udp not in list_output_udp:
                    list_udp_close.append(udp)
            for udp in list_output_udp:
                if udp not in list_udp_tmp:
                    list_udp_open.append(udp)
            #
            date_time_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f+0700")
            list_change_port =[]
            if len(list_tcp_open) !=0 :
                json_tcp_open = '{"time_stamp":"'+str(date_time_now)+'","state":"open","type_port":"tcp","port":"'+str(list_tcp_open)+'","dest_ip":"'+hostname_ip+'"}'
                list_change_port.append(json_tcp_open)
            if len(list_tcp_close) !=0 :
                json_tcp_close = '{"time_stamp":"'+str(date_time_now)+'","state":"close","type_port":"tcp","port":"'+str(list_tcp_close)+'","dest_ip":"'+hostname_ip+'"}'
                list_change_port.append(json_tcp_close)
            if len(list_udp_open) !=0 :
                json_udp_open = '{"time_stamp":"'+str(date_time_now)+'","state":"open","type_port":"udp","port":"'+str(list_udp_open)+'","dest_ip":"'+hostname_ip+'"}'
                list_change_port.append(json_udp_open)
            if len(list_udp_close) !=0 :
                json_udp_close = '{"time_stamp":"'+str(date_time_now)+'","state":"close","type_port":"udp","port":"'+str(list_udp_close)+'","dest_ip":"'+hostname_ip+'"}'
                list_change_port.append(json_udp_close)
            change_port_write = "\n".join(list_change_port)+"\n"
            writefile("Output/ATTT_port_change.log",change_port_write)
            return list_change_port             
    except:
        return []
        
