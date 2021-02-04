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
		
def GetSelection( count):
	reply = str(input('Type the number of the server to restart (1,2...) or "a" for All servers: ')).lower().strip()
	print (reply[0])
	if reply[0] == 'a':
		return 'a'
	else:
		if (int(reply[0]) >0) and (int(reply[0]) <= count):
			return int(reply[0])

		else:
			return Selection("Uhhhh... please enter ")



username="root"

localpath= "c:\\git-repo\\java-web\\customer_rest\\target\\"
file_name="CustomerRestServices"
jar_file = file_name+".jar"
remotepath="/"

#
# Get file last modification date
#

fileStatsObj = os.stat ( localpath+jar_file )
 
modificationTime = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
 

#
# Get the server list.
#
with open('deploy_params.json') as f:
  data = json.load(f)

servers = data.get("servers")

print ("Servers to be restarted:\n")
i=1
for serv in servers:
	print ("%i: %s" % (i,serv))
	i+=1


print ("\n")
sel = GetSelection( len(servers))
	
if yes_or_no("Are you sure you want to restart these servers"):
	password= getpass.getpass()
	if sel=='a' :

		for i in range(len(servers)): 
			#
			# Try to connect to the host.
			# Retry a few times if it fails.
			#
			server = servers[i]
			print ("Trying to connect to %s (%i/%i)" % (server, i+1, len(servers)))

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
				time.sleep(2)


			# If we could not connect within time limit
			if i == 4:
				print ("Could not connect to %s. Giving up" % server)
				sys.exit(1)
			print ("Wait for 5 seconds")
			time.sleep(5)

	else:
		server = servers[sel-1]
		print ("Trying to connect to %s " % (server))

		try:   
			ssh = paramiko.SSHClient() 
			ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(server, username=username, password=password)
			print ("Connected to %s" % server)

			
		except paramiko.AuthenticationException:
			print ("Authentication failed when connecting to %s" % server)
			sys.exit(1)
		except:
			print ("Could not SSH to %s, waiting for it to start" % server)
			time.sleep(2)
		
	#=== Restart the program
	stdin, stdout, stderr = ssh.exec_command('systemctl restart customer_rest.service')
	print ("Sent command ""systemctl start customer_rest.service""")
	ssh.close()


input("Press Enter to continue...")





