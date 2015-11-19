#!/usr/bin/env python2
import sys, os, requests, hashlib, json, shutil, zipfile, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force",
    help="Forces the update, even if you already have that version installed",
    action="store_true")
parser.add_argument("-c", "--clean",
    help="Clean all downloaded mods (WIP)",
    action="store_true")
args = parser.parse_args()

#Check to make sure we are running from the right directory
if not os.path.exists("dlib"):
    print("Error, please run this script from its base directory!.")
    sys.exit()

import dlib

dlib.checkstructure()
data, config = dlib.loadconfig()
dlib.checkupdate(config)

mod_database = config["moddbdir"]
modcachedir = config["cachedir"]
servermoddir = config["servermoddir"]

#Who needs error detection anyway
print("\nStarting SuperSolderDeploy")
print("Using solder instance: {0}".format(config["solderurl"]))
print("Modpack name: {0}".format(config["modpackname"]))
print("Server mods folder: ".format(config["servermoddir"]))
print("Currently installed modpack version: {0}".format(data["last"]))

print("\nChecking solder for new version...")
index = requests.get(config["modpackurl"])
index = index.json()

mpversion = index["recommended"]
print("\nNewest modpack version: {}\n".format(mpversion))

if mpversion == data["last"] and args.force == False:
    print("Already updated to this version, use -f to force update")
    sys.exit()
if args.force:
    print("Force mode enabled, force updating server mods...\n")

modindex = requests.get(config["modpackurl"] + index["recommended"])
modindex = modindex.json()

modinfo = {}

for i in dlib.tqdm(modindex["mods"], desc="Downloading Mod Info", leave=True):
    mod = requests.get(config["modsurl"] + i["name"])
    modinfo[i["name"]] = mod.json()

def generate_filename(i):
    st = "{name}-{version}.zip".format(name=i["name"], version=i["version"])
    return st

def download_file(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

def md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

msgs = []
for i in dlib.tqdm(modindex["mods"], desc="Downloading Mods", leave=True):
    info = modinfo[i["name"]]

    if not "#clientonly" in info["description"]:
        if not os.path.exists(os.path.join(mod_database, generate_filename(i))):
            download_file(i["url"], os.path.join(mod_database, generate_filename(i)))
            dlhash = md5(os.path.join(mod_database, generate_filename(i)))
            if not dlhash == i["md5"]:
                msgs.append("Warning, {0} does not match the hash".format(info["pretty_name"]))

        zipf = zipfile.ZipFile(os.path.join(mod_database, generate_filename(i)), "r")
        zipf.extractall(modcachedir)

    else:
        msgs.append("Skipped client only mod: "+info["pretty_name"])

for i in msgs:
    print(i)

modlocation = os.path.join(modcachedir, "mods")
modfiles = os.listdir(modlocation)

oldmpversion = data["last"]

data["last"] = mpversion
data["filelists"][mpversion] = modfiles

if oldmpversion == False:
    for i in modfiles:
        fl = os.path.join(modcachedir, "mods", i)
        if not i == "1.7.10":
            shutil.copy(fl, servermoddir)
else:
    oldfiles = data["filelists"][oldmpversion]

    print("Cleaning up old mods from server dir")
    for i in oldfiles:
        l = os.path.join(servermoddir, i)
        if not os.path.exists(l):
            print("Failed to remove file: "+l)
        else:
            os.remove(os.path.join(servermoddir, i))

    for i in modfiles:
        fl = os.path.join(modcachedir, "mods", i)
        if not i == "1.7.10":
            shutil.copy(fl, servermoddir)

dlib.saveconfig(data)