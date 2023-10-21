# Environment Preparation

## Please follow the below step in exact order to prepare a GCP environment for this course


## Installing VS Code
Download and Install from [here](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/)

## Generating and adding a SSH Key

1. Download Git Bash from [here](a.	https://git-scm.com/download/win). It will help you run linux command from a Windows Environment
2. Launch Git bash
3. Go to user/<user_name>/ folder on your windows machine using “cd” commands of linux syntax
4. Create a folder named “.ssh” in this location, if it doe not already exist
5. Run the below command:
```
ssh-keygen -t rsa -f gcp -C <user_name> -b 2048
```
6. Leave passphrase empty
7. It will create two files - "gcp" and "gcp.pub"
8. Login to Google cloud platform
9. Go to product product catalog from hamburger menu on top left, select VM instance
10. GCP will ask you to enable the product, enable it
11. Again, from the left go to metadata
![plot](/images/SSH-1.jpg)
12.	Click on Add SSH Key
![plot](/images/SSH-2.jpg)
13.	Got to Git bas and run
a.	cat gcp.pub
14.	This command will display the public part of the key on the screen
15.	Copy it
16.	Paste in the GCP window in the field and hit save
![plot](/images/SSH-3.jpg)


## Creating a Firewall rule in GCP:

1.	Got to VPC network from left hand side hamburger menu
![plot](/images/FW-1.jpg)
2.	Click on “Firewall” from left menu list
3.	Click on “Create Firewall Rule”
![plot](/images/FW-2.jpg)
4.	Select following configurations:
![plot](/images/FW-3.jpg)
![plot](/images/FW-4.jpg)
![plot](/images/FW-5.jpg)
5.	Hit Create


## Creating VM instance on GCP:

1.	Now to back to “VM Instances” from left hand side hamburger menu
![plot](/images/VM-1.jpg)
2.	Click on “Create Instance”
![plot](/images/VM-2.jpg)
3.	Put a name of your choice
4.	Select these configurations for region and machine configurations
![plot](/images/VM-3.jpg)
5.	Select below configurations for machine type
![plot](/images/VM-4.jpg)
6.	In the boot disk section click “Change”
![plot](/images/VM-5.jpg)
7.	Put the below configuration
![plot](/images/VM-6.jpg)
8.	Hit select
9.	In identity and API section click “Allow full access to all Cloud APIs”
![plot](/images/VM-7.jpg)

10.	Click on Advanced Options
11.	Click on “Network” section and in “Network Tags” put the same tag that you used to create the Firewall Rule. This will ensure that the created Firewall rule is used
12.	Keep all other settings as default and create the VM instance by clicking “Create” button at the bottom


## SSH into the VM instance:

1.	Note the external IP of the created VM instance
![plot](/images/VSSH-1.jpg)
2.	Open Git bash and type below command. Note that you need to use the exact same user name you used to create the SSH key in the beginning
```
ssh -i ~/.ssh/gcp <user_name>@<external_ip>
```
3.	Note that external_ip changes each time you restart the VM instance, so ensure that when you run this command you use the latest external IP


## Getting the VM instance ready to code:

### Step 1 Download and install Anaconda	
1. Once you have SSH-ed into the VM, install Anaconda (distribution of Python) by running below commands:
```sh
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
```
2. Once Anaconda3 is installed, type “exit” to exit the SSH connection with VM and login again
### Step 2 Update existing packages

```sh
sudo apt update
```
### Step 3 Install docker
```sh
sudo apt install docker.io
```
### Step 4 Install docker-compose:

1. Create a new directory

```sh
mkdir soft
cd soft
```

2. Run the below command to download docker-compose

```sh 
wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O docker-compose
```

3. Make it executable by running the below command

```sh 
chmod +x docker-compose
```
4. Add “soft” directory to the PATH environment variable

Open .bashrc file in edit mode
```sh
vi ~/.bashrc
```
Press “I” button from keyboard to start edit mode

Got to the last line and add below line:

```sh 
export PATH="${HOME}/soft:${PATH}"
```

Press “esc” key and type “:wq”

Press enter, this command will save the added line and exit the bashrc file

5. To run docker without “sudo”, run the below commands
```sh 
sudo groupadd docker
sudo usermod -aG docker $USER
```
6. Exit the VM instance and SSH again

7.	Run docker, to test it
```sh 
docker run hello-world
```
8. b.	If you get docker: docker: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create": dial unix /var/run/docker.sock: connect: permission denied. error, restart your VM instance from GCP 



## Setting up config file for easier SSH login:

1. Start a new git bash window, dont login to VM. In git bash go to .ssh folder
2. Start a file called config by running following command
```sh 
Vi config
```
3. Press “I” to go to insert mode
4. Paste the following content
```sh 
Host vm-descipr-2023
  HostName 34.100.159.229
  IdentityFile ~/.ssh/gcp
  User mouba
```
5. What it does it, it names the SSH connection with whatever you provide with keyword “Host”, I have provided “vm-descipr-2023”. You can chose any text for your Host. HostName is the public IP of the VM instance. Identity file is the private key generated in the begining
6. Save the file
7. Now, in the git bash window type
```sh 
ssh <host_name> 
```
8. In my case I will type:
```sh 
ssh vm-descipr-2023
```
9. REMEMBER: With each restart of the VM instance, the public IP will change, you will have to come to this location and change the public IP before logging in. 

## Connecting VM to VS code:

1.	Launch VS code and install and extension called “Remote-SSH” install it
2.	Click here (green circle at bottom left)
![plot](/images/VS-1.jpg)
3. Click on “connect to host”
![plot](/images/VS-2.jpg)
4. it will show the hostname you have added in the config file
![plot](/images/VS-3.jpg)
5. Click on the host name, wait for connection to establish
6. Once the connection is established, you basically are accessing VM instance from VS code and write all your codes here from local

