import configparser, json

numErrors = 0
config = configparser.ConfigParser()
config.read("/mnt/sage/disks.ini")
for s in config.sections():
    e = config[s]['numErrors'].replace('"','')
    numErrors += int(e)
    if not config[s]['status'].startswith('"DISK_NP'):
       if config[s]['status'] != '"DISK_OK"':
           result = {"result":"{}:{}".format(s,config[s]['status'])}
       else:
           result = {"result":"Ok"}
result['numErrors'] = numErrors
print(json.dumps(result))