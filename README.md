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
The `deploy_params.json` allows you to list all servers where the app will be deployed
```
{   
"servers": ["172.21.10.13", "172.21.10.14"]
}
```
### Depedencies
The code requires the `paramiko library`. Instalation instruction for the library can be found [here](http://www.paramiko.org/installing.html)

## Pending Issue
The app details are still not been passed in the JSON parameter file 
