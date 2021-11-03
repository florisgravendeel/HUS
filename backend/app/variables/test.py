from dotenv import find_dotenv, load_dotenv
import os


ENV_FILE = find_dotenv()
print("Finding env...." + ENV_FILE)
print(os.getcwd())
if ENV_FILE:
    print("Env found!")
    load_dotenv(ENV_FILE)
else:
    print("NO!! :( ENV NOT FOUND")


ENV_FILE = find_dotenv()
print("Finding env...." + ENV_FILE)
print(os.getcwd())
if ENV_FILE:
    print("Env found!")
    load_dotenv(ENV_FILE)
else:
    print("NO!! :( ENV NOT FOUND")

