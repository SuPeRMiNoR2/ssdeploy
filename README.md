# SuperSolderDeploy (ssdeploy)
ssdeploy is a script to update a minecraft server mods folder from a technic solder instance. 
This allows you to keep a modpack server up to date with a technic modpack, without having to 
manually update the server mods each time you change the client mods.

ssdeploy supports marking mods as client only, so that it does not download client only mods 
into the server mod folder. To mark a mod as client only, put the string #clientonly anywhere 
in the mods description on solder.


Warning: This script was developed on linux, for linux, however, as far as I am aware it does work on windows.

### Installation
* Install the python module "requests" from pip: `pip3 install requests`
* Clone it: `git clone https://github.com/SuPeRMiNoR2/ssdeploy.git`
* Change to the ssdeploy directory
* Run ssdeploy.py
* Edit config.ini
* Run ssdeploy again

### Configuration
By default, the configuration directory is located at `$HOME/.config/ssdeploy`
All of the data files will be located inside that directory, including the main config file, config.ini

ssdeploy also supports custom configuration directories that you can specify with --config /full/path/here 
It will create the directory if it does not exist, as long as the base directory does exist. 
This feature allows you to run multiple servers without conflict.

## ssdeploy requires python3!
