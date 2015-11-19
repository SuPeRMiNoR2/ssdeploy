import os, json, shutil, ConfigParser

requiredfolders = ["data", "data/db", "data/cache"]

datafile = "data/db.json"
configfile = "data/config.ini"

def checkstructure():
    for i in requiredfolders:
        if not os.path.exists(i):
            print("Making folder: {0}".format(i))
            os.mkdir(i)

    if os.path.exists(modcachedir):
        print("Cleaning cache dir")
        shutil.rmtree(modcachedir)
    os.mkdir(modcachedir)

def loadconfig():
    if not os.path.exists(configfile):
        print("Creating default config file.")
        Config = ConfigParser.ConfigParse()
        f = open(configfile, "w")
        Config.add_section("locations")
        Config.set("locations", "servermoddir", "replaceme")
        Config.set("locations", "solderapiurl", "replaceme")
        Config.write(configfile)
        f.close()

    Config = ConfigParser.ConfigParse()
    Config.read(configfile)
    cdb = {}

    cdb["servermoddir"] = Config.get("locations", "servermoddir")
    cdb["solderapiurl"] = Config.get("locations", "solderapiurl")

    if cbd.servermoddir == "replaceme":
        print("Please configure the settings in data/config.ini")
        sys.exit()
    elif os.path.exists(cbd.servermoddir) == False:
        print("The set server mod directory does not exist!")
        sys.exit()

    base = os.getcwd()
    cdb["modbdir"] = os.path.join(base, "data", "db")
    cdb["cachedir"] = os.path.join(base, "data", "cache")

    if os.path.exists(datafile):
        f = open(datafile)
        data = json.load(f)
        f.close()
    else:
        data = {"filelists": {}, "last": False}

    return data, cdb

def saveconfig(data)
    f = open(datafile, "w")
    json.dump(data, f)
    f.close()
