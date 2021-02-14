import sys
import os

if os.path.exists("web"):
    sys.path.append("web")
from web_main import app

if __name__ == "__main__":
    app.run()
