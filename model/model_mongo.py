
from pymongo import MongoClient
import yaml

### Get Config YAML File
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONFIG_FILE = './config.yaml'

try:
    file_stream = open(CONFIG_FILE, "r")
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)

def connect_mongodb():
    try:
        mongo_user = Config['mongodb']['username']
        mongo_pass = Config['mongodb']['password']
        host = Config['mongodb']['host']
        cluster = MongoClient("mongodb://"+ mongo_user + ":"+ mongo_pass +"@"+ host+"/?directConnection=true&authMechanism=DEFAULT&authSource=healthscore")
        return cluster
    except Exception as e:
        print(e)