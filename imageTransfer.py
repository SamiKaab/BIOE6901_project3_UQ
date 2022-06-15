import subprocess
import os



def scp(pathSource,pathDestination,pwd,usr,host):
    print("sshpass", "-p"  + " " +  pwd  + " " +  "scp", "-r"  + " " +  "{}@{}:{}".format(usr,host,pathSource) + " " + pathDestination)
    p = subprocess.Popen(["sshpass", "-p", pwd,"scp", "-r", "{}@{}:{}".format(usr,host,pathSource), pathDestination])
    sts = os.waitpid(p.pid, 0)

