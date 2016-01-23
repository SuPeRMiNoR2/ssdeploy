import platform
major = platform.python_version_tuple()[0]

import os, json, shutil, sys, requests

if major == 2:
        import ConfigParser
else:
        import configparser as ConfigParser

requiredfolders = ["~/.config", "~/.config/ssdeploy", "~/.config/ssdeploy", "~/.config/ssdeploy/db", "~/.config/ssdeploy/cache"]

base = os.path.expanduser("~/.config/ssdeploy")

datafile = os.path.join(base, "db.json")
configfile = os.path.join(base, "config.ini")
cachedir = os.path.join(base, "cache")
moddbdir = os.path.join(base, "db")
cachedir = os.path.join(base, "cache")

def checkupdate(config):
    f = open("version.txt", "rb")
    currentversion = f.read()
    f.close()

    versionurl = "https://raw.githubusercontent.com/SuPeRMiNoR2/ssdeploy/master/version.txt"
    r = requests.get(versionurl)
    if not currentversion == r.content:
        if config["autoupdate"] == "true":
            print("-----------------------------------------------")
            print("Updating ssdeploy.")
            os.system("git pull")
            print("Done, please restart ssdeploy")
            print("-----------------------------------------------")
            sys.exit()
        else:
            print("-----------------------------------------------")
            print("ssdeploy update availible! Please run git pull")
            print("-----------------------------------------------")

def checkstructure():
    for i in requiredfolders:
        i = os.path.expanduser(i)
        if not os.path.exists(i):
            print("Making folder: {0}".format(i))
            os.mkdir(i)

    if os.path.exists(cachedir):
        shutil.rmtree(cachedir)
    os.mkdir(cachedir)

def loadconfig():
    if not os.path.exists(configfile):
        print("Creating default config file.")
        Config = ConfigParser.ConfigParser()
        f = open(configfile, "w")
        Config.add_section("locations")
        Config.add_section("system")
        Config.set("locations", "servermoddir", "replaceme")
        Config.set("locations", "solderurl", "replaceme")
        Config.set("locations", "modpackname", "replaceme")
        Config.set("system", "autoupdate", "false")
        Config.write(f)
        f.close()

    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    cdb = {}

    cdb["servermoddir"] = Config.get("locations", "servermoddir")
    cdb["solderurl"] = Config.get("locations", "solderurl")
    modpack = Config.get("locations", "modpackname")
    cdb["modpackname"] = modpack
    cdb["autoupdate"] = Config.get("system", "autoupdate")

    if not cdb["solderurl"][-1] == "/":
        cdb["solderurl"] = cdb["solderurl"] + "/"

    cdb["modpackurl"] = "{base}api/modpack/{modpack}/".format(base=cdb["solderurl"], modpack=modpack)
    cdb["modsurl"] = "{base}api/mod/".format(base=cdb["solderurl"])

    if cdb["servermoddir"] == "replaceme":
        print("Please configure the settings in {0}".format(configfile))
        sys.exit()

    if not os.path.exists(cdb["servermoddir"]):
        print("The set server mod directory ({0}) does not exist!".format(cdb["servermoddir"]))
        sys.exit()

    cdb["moddbdir"] = moddbdir
    cdb["cachedir"] = cachedir
    
    if os.path.exists(datafile):
        f = open(datafile)
        data = json.load(f)
        f.close()
    else:
        data = {"filelists": {}, "last": False}

    return data, cdb

def saveconfig(data):
    f = open(datafile, "w")
    json.dump(data, f)
    f.close()
