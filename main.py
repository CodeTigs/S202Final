import os

from dotenv import load_dotenv

load_dotenv()   # isso carrega MONGO_URI, NEO4J_URI etc antes de qualquer import

from cli.menu import menu

if __name__ == "__main__":
    menu()

