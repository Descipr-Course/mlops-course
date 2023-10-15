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

