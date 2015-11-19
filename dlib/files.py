import os, json, shutil, ConfigParser, sys, requests

requiredfolders = ["data", "data/db", "data/cache"]

base = os.getcwd()

datafile = os.path.join(base, "data", "db.json")
configfile = os.path.join(base, "data", "config.ini")
cachedir = os.path.join(base, "data", "cache")

def checkupdate():
    f = open("version.txt")
    currentversion = f.read()
    f.close()

    versionurl = "https://raw.githubusercontent.com/SuPeRMiNoR2/ssdeploy/master/version.txt"
    r = requests.get(versionurl)
    if not currentversion == r.content:
        print("New version availible! Please run git pull")

def checkstructure():
    for i in requiredfolders:
        if not os.path.exists(i):
            print("Making folder: {0}".format(i))
            os.mkdir(i)

    if os.path.exists(cachedir):
        print("Cleaning cache dir")
        shutil.rmtree(cachedir)
    os.mkdir(cachedir)

def loadconfig():
    if not os.path.exists(configfile):
        print("Creating default config file.")
        Config = ConfigParser.ConfigParser()
        f = open(configfile, "w")
        Config.add_section("locations")
        Config.set("locations", "servermoddir", "replaceme")
        Config.set("locations", "solderurl", "replaceme")
        Config.set("locations", "modpackname", "replaceme")
        Config.write(f)
        f.close()

    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    cdb = {}

    cdb["servermoddir"] = Config.get("locations", "servermoddir")
    cdb["solderurl"] = Config.get("locations", "solderurl")
    modpack = Config.get("locations", "modpackname")
    cdb["modpackname"] = modpack

    if not cdb["solderurl"][-1] == "/":
        cdb["solderurl"] = cdb["solderurl"] + "/"

    cdb["modpackurl"] = "{base}api/modpack/{modpack}/".format(base=cdb["solderurl"], modpack=modpack)
    cdb["modsurl"] = "{base}api/mod/".format(base=cdb["solderurl"])

    if cdb["servermoddir"] == "replaceme":
        print("Please configure the settings in data/config.ini")
        sys.exit()

    if not os.path.exists(cdb["servermoddir"]):
        print("The set server mod directory ({0}) does not exist!".format(cdb["servermoddir"]))
        sys.exit()

    base = os.getcwd()
    cdb["moddbdir"] = os.path.join(base, "data", "db")
    cdb["cachedir"] = os.path.join(base, "data", "cache")

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
