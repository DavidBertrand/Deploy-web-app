# Deploy-web-app
Allows to deploy new compiled code to Web servers

## Instructions
This python code will automate the tasks required to deploy a java web application on each web servers servicing that application

### Tasks:
```
* Get login access to the web server through **SSH**
* Backup the running application in the event it needs to be rolled back
* Copy the new compiled application to the web server
* Restart the application service
```
### Parameters
The `deploy_params.json` allows you to define the application and deploymeent specifics:
```
{   
    "app_name":"CustomerRestServices",
    "app_ext":"jar",
    "servers": ["172.21.10.13", "172.21.10.14"],
    "localpath":"c:\\git-repo\\customer_rest\\target\\",
    "remotepath":"/",
    "ssh_key_filename":"some path"
}
```
* app_name: Name of the application file 
* app_ext: application file extention
* servers: list of servers where the app will be deployed
* localpath: local path where the application to deploy is
* remotepath: path on servers where the app needs to be deployed
* ssh_key_filename: path to the ssh key when one is needed for the connection

### Depedencies
The code uses python 3.8 and the `paramiko library`. Installation instruction for the library can be found [here](http://www.paramiko.org/installing.html)


### Pending Issues
when the password is wrong the error handling needs to be looked at