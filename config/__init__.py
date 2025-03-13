import pathlib

import environ

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")
