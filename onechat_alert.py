# from datetime import datetime
from module.get_mongodb import get_data_mongo

def main():
    try:
        get_data_mongo()
        print("Available !!!")
    except Exception as e:
        print(e)


main()