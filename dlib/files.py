import os, json, shutil, sys, requests
import configparser as ConfigParser

defaultconfig = {"locations": {"servermoddir": "replaceme", "solderurl": "replaceme", "modpackname": "changeme"}, 
        "system": {"autoupdate": "false", "configupdate": "false"}, "configupdate": {"configupdatemode": "false", "configmodstub": "changeme", "configdir": "changeme"}}

def init_paths(args):
    global base
    global datafile 
    global configfile 
    global cachedir
    global moddbdir

    if args.config:
        base = os.path.abspath(args.config)
        print("Using alternate config directory {0}".format(base))
    else:
        base = os.path.expanduser("~/.config/ssdeploy")
        print("Using default config directory")

    datafile = os.path.join(base, "db.json")
    configfile = os.path.join(base, "config.ini")
    cachedir = os.path.join(base, "cache")
    moddbdir = os.path.join(base, "db")

    requiredfolders = ["", "db", "cache"] #The first one makes the base directory
    checkstructure(requiredfolders, args)

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

def checkstructure(paths, args):
    if not args.config:
        if not os.path.exists(os.path.expanduser("~/.config")):
            os.mkdir(os.path.expanduser("~/.config"))
    for i in paths:
        b = os.path.join(base, i)
        if not os.path.exists(b):
            print("Making folder: {0}".format(b))
            os.mkdir(b)

    if os.path.exists(cachedir):
        shutil.rmtree(cachedir)
    os.mkdir(cachedir)

def readini(configfile):
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    return Config

def writeini(configfile, cinst):
    f = open(configfile, "w")
    cinst.write(f)
    f.close()

def mapini(cinst):
    cdb = {}
    adb = {}
    sections = cinst.sections()
    for section in sections:
        sdata = {}
        options = cinst.options(section)
        for option in options:
            sdata[option] = cinst.get(section, option)
            adb[option] = sdata[option]
        cdb[section] = sdata
    return adb, cdb #I return in the wrong order to keep compat with the main module

def loadconfig():
    if not os.path.exists(configfile):
        print("Creating default config file.")
        Config = ConfigParser.ConfigParser()
        Config.add_section("init")
        Config.set("init", "setup", "To begin, set the correct paths in all the variables that say changeme.")
        writeini(configfile, Config)
    else:
        Config = readini(configfile)

    sections = Config.sections()
    for s in defaultconfig:
        if not s in sections:
            print("Adding section to config file: {}".format(s))
            Config.add_section(s)
    sections = Config.sections
    for s in defaultconfig:
        options = Config.options(s)
        for o in defaultconfig[s]:
            if not o in options:
                print("Adding entry {0} to section {1}".format(o, s))
                Config.set(s, o, defaultconfig[s][o])
    f = open(configfile, "w")
    Config.write(f)
    f.close()

    cdb, adb = mapini(Config)
    modpack = cdb["modpackname"]

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

    return data, cdb, adb

def saveconfig(data):
    f = open(datafile, "w")
    json.dump(data, f)
    f.close()
