# ansible-webhook-proxy

This project is used to set up a proxy service that integrates ansible tower with bitbucket webbhooks.

The proxy is developed using python which reads the configuration from a json file.

## Prerequisites

Make sure you have installed all of the following prerequisites on your target machine

* Python - [ Download & Install Python (>3.5) ](https://www.python.org/downloads/). Linux machines typically have this already installed

* Pip - Pip is the package installer for Python.

#### Pip installation

To install the pip, run the below command
```
yum install python3-pip
```


## Installation

There are 2 methods of Installation for the webhook proxy.

* Manual Installation
* Using a Playbook

Before you begin with the two available methods, you need to clone the repository, update the configuration file and proceed with the preferred mode of installation.

Once the repository is cloned, all the steps should be performed within the cloned repository.

#### Cloning the Repository
```
git clone https://github.com/yashfaizan/webhook-proxy.git
```

#### Configuration File

The webhook configuration is controlled using the file ```webhook-config.json```. Below are the details of the varibales in the configuration file

| Variable Name | Description |
| ------------- | ----------- |
| server_ip     | The ip address for the webhook server |
| port          | The port the webhook will listen on |
| logfile | The full path of the bitbucket webhook logfile |
| routes/ *routename* / url | The url of the ansible tower job to trigger |
| routes/ *routename* / credential | The credential to use to trigger the ansible job |
| routes/ *routename*/ webhook_secretkey | The secretkey to validate the request and payload from the bitbucket |
| credentials/ *credential name* / url_username | The username used to login to ansible tower |
| credentials/ *credential name* / url_password | The password used to authenticate the ansible tower with the given username. Here the password should be base64 encoded format |

#### Example config: 
```
{
	"server_ip": "10.128.0.11",
	"port": 5000,
	"logfile": "/root/webhook/bitbucket-webhook.log",
	"routes": {
		"patch": {
			"url": "http://10.128.0.11/api/v2/job_templates/296/launch/",
			"credential": "tower_account",
			"webhook_secretkey": "somesecretkey"
		},
		"autoconfig": {
			"url": "http://10.128.0.11/api/v2/job_templates/296/launch/",
			"credential": "tower_account2",
			"webhook_secretkey": "somesecretkey"
		}
	},
	"credentials": {
		"tower_account": {
			"url_password": "UGFzc3dvcmRAMTIzNDUh",
			"url_username": "admin"
		},
		"tower_account2": {
			"url_password": "UGFzc3dvcmRAMTIzNDUh",
			"url_username": "admin"
		}
	}
} 

```
## Manual Installation

The below steps can be followed once you have downloaded and installed python and pip on target server.

### Installing Dependencies

* Requirements file - This file contains all the required packages needed to run the project.

To install all the dependencies required for proxy, run the below command within the cloned repository.
```bash
pip3 install --proxy www-cache.reith.bbc.co.uk:80 -r requirements.txt
```

### Running the proxy as a service

To create a service file, make sure you have access to the path /etc/systemd/service/. Create a file with extension **.service**(webhook-proxy.service). Copy the contents present in the reference file **webhook-proxy.service** and update the below configurations accordingly.

- set your actual username after User=
- set the proper path to your script in ExecStart=
- ExecStart= < path where python is installed > < full path of the setup_proxy.py>

#### Example 
```
ExecStart= /usr/bin/python3.6 /data/webhook/api/proxy_server.py
```
That's it. We can now start the service

```bash
systemctl start webhook-proxy   ### systemctl start < file name >  do not include extension .service with systemctl
```
And automatically get it to start on boot

```bash
systemctl enable webhook-proxy
```

## Using Playbook

The webhook proxy can also be deployed using Ansible Playbook. Update the **webhook-hostsfile** with the target server details and run the below command.

```bash
ansible-playbook -i webhook-hostsfile deploy-proxy.yml -e"webhook_proxy_directory=/tmp/webhook/"
```

Click on role for detailed description

| Role Name | Brief description |
|-----------|-------------------|
|[role_deploy_webhook_proxy](role_deploy_webhook_proxy/README.md) | This role deploys a proxy as a service |