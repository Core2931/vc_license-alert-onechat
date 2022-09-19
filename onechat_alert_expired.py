
# from datetime import datetime, timedelta, date
from module.get_mongodb import get_data_mongo_expired


def main():
    try:
        get_data_mongo_expired()
        print("Expired data !!!")
    except Exception as e:
        print(e)


main()