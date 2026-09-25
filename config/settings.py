import os
class EnvConfig:
    def __init__(self, env):
        self.saucedemo_url =  os.getenv("SAUCE_DEMO_URL")
        self.demoqa_url = os.getenv("DEMO_QA_URL")
        self.jsonplaceholder_url = os.getenv("JSON_PLACEHOLDER_URL")