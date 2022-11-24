import subprocess
import os


###
# ssh file transfer
# 
# Variables
#   pathSource : source folder path
#   pathDestination : destination folder path
#   pwd : password
#   usr : username
#   host : host name or IP
def scp(pathSource,pathDestination,pwd,usr,host):
    print("sshpass", "-p"  + " " +  pwd  + " " +  "scp", "-r"  + " " +  "{}@{}:{}".format(usr,host,pathSource) + " " + pathDestination)
    p = subprocess.Popen(["sshpass", "-p", pwd,"scp", "-r", "{}@{}:{}".format(usr,host,pathSource), pathDestination])
    sts = os.waitpid(p.pid, 0)

