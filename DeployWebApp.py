import os
import paramiko
import getpass
import json
import time
import stat

from datetime import datetime 
from time import sleep

def yes_or_no(question):
	reply = str(input(question+' (y/n): ')).lower().strip()
	if reply[0] == 'y':
		return True
	if reply[0] == 'n':
		return False
	else:
		return yes_or_no("Uhhhh... please enter ")



username="root"

localpath= "c:\\git-repo\\customer_rest\\target\\"
file_name="CustomerRestServices"
jar_file = file_name+".jar"
remotepath="/"

#
# Get file last modification date
#

fileStatsObj = os.stat ( localpath+jar_file )
 
modificationTime = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
 
print("Last Modified Time : ",  ) 

#
# Get the server list.
#
with open('deploy_params.json') as f:
  data = json.load(f)

servers = data.get("servers")
print ("Application to be deployed: "+ file_name + "("+modificationTime+")")
print ("Server where the application will be deployed:")
for serv in servers:
	print (serv) 
	
if yes_or_no("Are you sure you want to launch the deployment?"):
	password= getpass.getpass()
	for serv in servers:
		#
		# Try to connect to the host.
		# Retry a few times if it fails.
		#
		i=1
		while True:
			server = serv
			print ("Trying to connect to %s (%i/30)" % (server, i))

			try:   
				ssh = paramiko.SSHClient() 
				ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(server, username=username, password=password)
				print ("Connected to %s" % server)
				break
				
			except paramiko.AuthenticationException:
				print ("Authentication failed when connecting to %s" % server)
				sys.exit(1)
			except:
				print ("Could not SSH to %s, waiting for it to start" % server)
				i += 1
				time.sleep(2)

		# If we could not connect within time limit
		if i == 30:
			print ("Could not connect to %s. Giving up" % server)
			sys.exit(1)


		#=== 1) backup old jar
		now = datetime.now()
		dt_string = now.strftime("%Y%m%d_%H%M%S")

		command='cp '+ remotepath + jar_file +' '+remotepath + file_name +'_'+ dt_string +".jar"
		stdin, stdout, stderr = ssh.exec_command(command)
		print ("Sent command "+ command)
		#=== 2) Upload new jar
		sftp = ssh.open_sftp()
		sftp.put(localpath+jar_file, remotepath+jar_file)
		sftp.close()
		print ("Uploaded  "+ jar_file)

		#=== 3)Restart the program
		stdin, stdout, stderr = ssh.exec_command('systemctl restart customer_rest.service')
		print ("Sent command ""systemctl start customer_rest.service""")
		ssh.close()


input("Press Enter to continue...")





