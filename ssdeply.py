#!/usr/bin/env python2
import sys, os, requests, hashlib, json, shutil, zipfile

#Check to make sure we are running from the right directory
if not os.path.exists("dlib"):
    print("Error, please run this script from its base directory!.")
    sys.exit()

cwd = os.getcwd()
import dlib
dlib.checkstructure()

data, config = dlib.loadconfig()


mod_database = config["moddbdir"]
modcachedir = config["cachedir"]
servermoddir = config["servermoddir"]
solderapi = config["solderapiurl"]

#Who needs error detection anyway

print("Downloading main mod info (this will take around 30 seconds)")
index = requests.get(solderapi)
index = index.json()

mpversion = index["recommended"]
print("Current modpack version: {}".format(mpversion))

if mpversion == data["last"]:
    error("Already updated to this version.")

modindex = requests.get("http://solder.pc-logix.com/api/modpack/pc-logix-17/" + index["recommended"])
modindex = modindex.json()

modinfo = {}

print("Downloading Extra mod info.")
for i in modindex["mods"]:
    mod = requests.get("http://solder.pc-logix.com/api/mod/"+i["name"])
    modinfo[i["name"]] = mod.json()
print("Done")

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

for i in modindex["mods"]:
    info = modinfo[i["name"]]

    if not "#clientonly" in info["description"]:
        if not os.path.exists(os.path.join(mod_database, generate_filename(i))):
            print("Downloading {0} version {1}".format(info["pretty_name"], i["version"]))
            download_file(i["url"], os.path.join(mod_database, generate_filename(i)))
            dlhash = md5(os.path.join(mod_database, generate_filename(i)))
            if not dlhash == i["md5"]:
                print("Warning, {0} does not match the hash")

        zipf = zipfile.ZipFile(os.path.join(mod_database, generate_filename(i)), "r")
        zipf.extractall(modcachedir)

    else:
        print("Skipping client only mod: "+info["pretty_name"])

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
            print("Report this")
        else:
            os.remove(os.path.join(servermoddir, i))

    for i in modfiles:
        fl = os.path.join(modcachedir, "mods", i)
        if not i == "1.7.10":
            shutil.copy(fl, servermoddir)

f = open(datafile, "w")
json.dump(data, f)
f.close()
