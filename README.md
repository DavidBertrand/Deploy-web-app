# Deploy-web-app
Allows to deploy new compiled code to Web servers

## Instructions
The code will automate the tasks required to deploy a java web application on each web servers servicing that application

### Tasks:
```
* Get login access to the web server through **SSH**
* Backup the running application in the event it needs to be rolled back
* Copy the new compiled application from the local machine to the web server
* Restart the application service
```
### Parameters
The `servers_test.json` allows you to list all servers needing the deployment
```
{   
"servers": ["172.21.10.13", "172.21.10.14"]
}
```
## Pending Issue
The app details are still no been passed in the JSON parameter file 
