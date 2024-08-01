from dotenv import load_dotenv
import os 

def load_env(v): 
    load_dotenv()
    return os.getenv(v) 