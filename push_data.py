from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import pymongo
import numpy as np
import pandas as pd
import certifi
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection

            # self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL, tlsCAFile=certifi.where())
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "network_data/phisingData.csv"
    DATABASE = "SINIYAAI"
    collection = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    # print(records)
    logging.info(f"Number of records: {len(records)}")
    logging.info(
        f"Sample record: {records[0] if records else 'No records found'}")
    no_of_records = networkobj.insert_data_mongodb(
        records, DATABASE, collection)
    print(no_of_records)
