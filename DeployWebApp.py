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
	reply = str(input('Type the number of the server where the App will be deployed (1,2...) or "a" for All servers: ')).lower().strip()
	print (reply[0])
	if reply[0] == 'a':
		return 'a'
	else:
		if (int(reply[0]) >0) and (int(reply[0]) <= count):
			return int(reply[0])

		else:
			return Selection("Uhhhh... please enter ")
			
def DeployAppToServer(server):
	try:   
		ssh = paramiko.SSHClient() 
		ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		if ssh_key_filename == None:
			print ("Using password")
			ssh.connect(server, username=username, password=password)
		else:
			print ("Using Key %s" % ssh_key_filename)	
			ssh.connect(server, username=username, passphrase=password, key_filename =ssh_key_filename)
			
		print ("Connected to %s" % server)

		
	except paramiko.AuthenticationException:
		print ("Authentication failed when connecting to %s" % server)
		sys.exit(1)
	except:
		print ("Could not SSH to %s, waiting for it to start" % server)
		i += 1
		time.sleep(2) 
		# If we could not connect within time limit
		if i == 5:
			print ("Could not connect to %s. Giving up" % server)
			sys.exit(1)


	#=== 1) backup old jar
	now = datetime.now()
	dt_string = now.strftime("%Y%m%d_%H%M%S")

	command='mv ' + remotepath + app_file +' '+remotepath + app_name +'_'+ dt_string +"."+app_ext
	stdin, stdout, stderr = ssh.exec_command(command)
	print ("Sent command "+ command)
	#=== 2) Upload new jar
	sftp = ssh.open_sftp()
	sftp.put(localpath+app_file, remotepath+app_file)
	sftp.close()
	print ("Uploaded  "+ app_file)

	#=== 3)Restart the program
	stdin, stdout, stderr = ssh.exec_command('systemctl stop customer_rest.service')
	print ("Sent command ""systemctl stop customer_rest.service""")
	time.sleep(0.33)
	stdin, stdout, stderr = ssh.exec_command('systemctl start customer_rest.service')
	print ("Sent command ""systemctl start customer_rest.service""")
	ssh.close()


username="root"

localpath= ""
file_name="CustomerRestServices"
jar_file = file_name+".jar"
remotepath="/"

 


#
# Get parameters from JSON file.
#
with open('deploy_params.json') as f:
  data = json.load(f)

servers = data.get("servers")
localpath= data.get("localpath")
app_name=data.get("app_name")
app_ext=data.get("app_ext")
app_file = app_name + "."+app_ext
remotepath=data.get("remotepath")
ssh_key_filename = data.get("ssh_key_filename")

#
# Get file last modification date
#

fileStatsObj = os.stat ( localpath+jar_file )
 
modificationTime = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )


print ("Application to be deployed: "+ app_file + "( Compiled date: "+modificationTime+")")
print ("Server where the application can be deployed:")

i=1
for serv in servers:
	print ("%i: %s" % (i,serv))
	i+=1


print ("\n")
sel = GetSelection( len(servers))
	
	
if yes_or_no("Are you sure you want to Depoly the app to this/these server(s)"):
	password= getpass.getpass()
	if sel=='a' :
		i=0
		for server in servers: 
			#
			# Try to connect to the host.
			# Retry a few times if it fails.
			#
			i+=1
			print ("Trying to connect to %s (%i/%i)" % (server, i, len(servers)))
			DeployAppToServer(server)
			if (i != len(servers)):
				#=== Sleep 2s before processing with the next server
				print ("Wait 10 seconds")	
				time.sleep(10)		
	
	else:
			server = servers[sel-1]
			print ("Trying to connect to %s " % (server))
			DeployAppToServer(server)


input("Press Enter to continue...")





