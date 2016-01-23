# SuperSolderDeploy (ssdeploy)
ssdeploy is a script to update a minecraft server mods folder from a technic solder instance. 
This allows you to keep a modpack server up to date with a technic modpack, without having to 
manually update the server mods each time you change the client mods.

ssdeploy supports marking mods as client only, so that it does not download client only mods 
into the server mod folder. To mark a mod as client only, put the string #clientonly anywhere 
in the mods description on solder.

Right now, the script is very beta, and very messy. I only put it on github to keep track of it. 

Notice: This script was developed on linux, for linux, and I am not sure if it will work on windows.

### Installation
* Install the python module "requests" from pip: `pip3 install requests`
* Clone it: `git clone https://github.com/SuPeRMiNoR2/ssdeploy.git`
* Change to the ssdeploy directory
* Run ssdeploy.py
* Edit data/config.ini
* Run ssdeploy again

## ssdeploy requires python3!
