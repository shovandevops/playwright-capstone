import os
from dotenv import load_dotenv
from config.settings import EnvConfig

def load_env():
    env = load_dotenv()
    return EnvConfig(env)