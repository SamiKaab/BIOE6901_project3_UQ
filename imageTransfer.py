import subprocess
import os



def scp(pathSource,pathDestination,pwd,usr,host):
    p = subprocess.Popen(["sshpass", "-p", pwd,"scp", "-r", pathSource, "{}@{}:{}".format(usr,host,pathDestination)])
    sts = os.waitpid(p.pid, 0)