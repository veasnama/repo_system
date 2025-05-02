from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
load_dotenv()


class ServerFirmwareInfo():
    def __init__(self):
        self.name = None
        self.version = None
        self.release_date = None
        self.server_type = None
        self.server_url = None
        self.support_type = ["T8-1", "X8-2", "S7-2", "X7-2"]

    def set_server_type(self, ser_type):
        self.server_type = ser_type

    def set_url(self, url):
        self.server_url = url

    def valid_server_type(self):
        if self.server_type not in self.support_type:
            return False
        else:
            return True

    def get_info(self):
        try:
            if self.valid_server_type():
                res = requests.get(self.server_url.__add__(
                    "#").__add__(self.server_type.upper()))
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')
                target_anchors = soup.select('a#'.__add__(self.server_type))
                for target_anchor in target_anchors:
                    target_row = target_anchor.find_parent('tr')
                    print(target_row)
# Print the captured rows
            else:
                return "Unsupport server type"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


server_request = ServerFirmwareInfo()
server_request.set_server_type("S7-2")
server_request.set_url(os.getenv("SERVER_URL"))
print(server_request.get_info())
