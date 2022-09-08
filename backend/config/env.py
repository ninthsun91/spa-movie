from dotenv import load_dotenv
import os


class Env:
    load_dotenv(override=True)
    get = os.environ.get

    DBG = get("FLASK_DEBUG")
    SKY = get("SECRET_KEY")
    URL = get("MongoDB_URL")
    HKY = get("HASH_KEY")
    NMV = get("NMovie_Search")
    CID = get("Client_ID")
    CSC = get("Client_Secret")