import os
import sys

# Add SMART_Service_Desk/app/ to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'SMART_Service_Desk/app')))

from SMART_Service_Desk.config import Config
from SMART_Service_Desk.app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
