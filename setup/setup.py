'''
Created on Jan 10, 2017

@author: sontn
'''
import os
def writefile(file_write,content):
    try:
        #path = os.getcwd()
	path = os.path.dirname(os.path.realpath(__file__))
        statinfo = os.stat(path)
        ## 
        f = open(file_write,"wb")
        f.close()
        os.chown(file_write, statinfo.st_uid, statinfo.st_gid)
        f = open(file_write,"wb")
        f.write(content)
        f.close()
    except:
        print "Except writefile"

def makefileyml(dir_path):
    #path = os.path.dirname(os.path.realpath(__file__))
    statinfo = os.stat(dir_path)
    f = open(dir_path,"wb")
    f.close()
    os.chown(dir_path, statinfo.st_uid, statinfo.st_gid)
    f = open(dir_path,"wb")
    f.write(dir_path)
    
def remove_string(line):
    try:
        list_replace =[" ","\t","\r","\n",'"',"'"]
        for string_replace in list_replace:
            line = line.replace(string_replace,"")
        return line
    except:
        return line
def readfileconfig():
    try:
        dict_config={}
        f = open("config.yml","r")
        lines = f.read()
        list_lines=lines.split('\n')
        for line in list_lines:
            line = str(remove_string(line))
            if not (line =="" or line[:1]=="#") :
                if ":" in line:
                    (key,val)= line.split(":")
                    dict_config[str(key)]=str(val)
        return dict_config
        ######### use dict_.update(dict1)
    except:
        return {}
def MakeConfigFilebeat():
    current_folder_path= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path_monitor_login = ""+str(current_folder_path)+"/monitorATTT/Output/ATTT_login_ssh.log"
    path_monitor_port = ""+str(current_folder_path)+"/monitorATTT/Output/ATTT_port_change.log"
    dict_ ={'port_document_type': 'attt_monitor_port', 
            'path_monitor_login': path_monitor_login, 
            'port_logstash': '5044', 
            'login_document_type': 'attt_monitor_login', 
            'path_monitor_cmdlog': '/var/log/attt_cmdlog.log', 
            'path_monitor_port': path_monitor_port, 
            'cmdlog_document_type': 'attt_monitor_cmdlog', 
            'host_logstash': '192.168.142.101'}
    dict_conf = readfileconfig()
    dict_.update(dict_conf)
    fileyml= ""+"filebeat.prospectors:"+"\n- input_type: log"+"\n  paths:"+"\n    - "+dict_["path_monitor_cmdlog"]+"\n  document_type: "+dict_["cmdlog_document_type"]
    fileyml= fileyml+ "\n- input_type: log"+"\n  paths:"+"\n    - "+dict_["path_monitor_login"]+"\n  document_type: "+dict_["login_document_type"]
    fileyml= fileyml+ "\n- input_type: log"+"\n  paths:"+"\n    - "+dict_["path_monitor_port"]+"\n  document_type: "+dict_["port_document_type"]
    fileyml= fileyml+"\noutput.logstash:"+"\n  enabled: true"+"\n  hosts: ["+'"'+dict_["host_logstash"]+":"+dict_["port_logstash"]+'"]'
    #return fileyml
    dir_filebeat = current_folder_path+"/filebeat/filebeat.yml"
    writefile(dir_filebeat,fileyml)
def Runfilebeat():
    try:
        current_folder_path= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        run_string = "nohup "+current_folder_path+"/filebeat/filebeat" +" -c "+current_folder_path+"/filebeat/filebeat.yml &"
        #print run_string
        os.system(run_string)
    except:
        pass
if __name__ == '__main__':
    MakeConfigFilebeat()
    Runfilebeat()
    #print os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print "OK"
