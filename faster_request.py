import requests
from bs4 import BeautifulSoup

url = "https://www.oracle.com/servers/technologies/firmware/release-history-jsp.html#T8-1"

try:
    with requests.get(url, timeout=5) as res:
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        target_anchor = soup.select_one('a#T8-1')
        t8_rows = []
        if target_anchor:
            table = target_anchor.find_parent('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        firmware_version = cells[0].get_text(strip=True)
                        if firmware_version:
                            t8_rows.append(f"Firmware: {firmware_version}")
                        download_info = cells[1].get_text(
                            strip=True, separator=" ")
                        if download_info:
                            t8_rows.append(f"Download: {download_info}")
        if t8_rows:
            with open("t8_firmware.txt", "w", buffering=8192) as file:
                file.write("\n".join(t8_rows))
            print("Data written to 't8_firmware.txt' successfully!")
            print(f"Extracted content: {t8_rows}")
        else:
            print("No rows found in the T8-1 section.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
