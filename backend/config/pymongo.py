from pymongo import MongoClient

from ..config import *


class Pymongo:
    client = MongoClient(Env.URL, tls=True, tlsAllowInvalidCertificates=True)
    db = client.spamovie