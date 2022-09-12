from dotenv import load_dotenv
import os


class Env:
    # load_dotenv(override=True)
    load_dotenv()
    get = os.environ.get

    DBG = "production"
    SKY = get("SECRET_KEY")
    URL = get("MongoDB_URL")
    HKY = get("HASH_KEY")
    NMV = get("NMovie_Search")
    CID = get("Client_ID")
    CSC = get("Client_Secret")