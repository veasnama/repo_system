import requests
from lxml import html
from io import BytesIO

# URL for SPARC firmware release history
url = "https://www.oracle.com/servers/technologies/firmware/release-history-jsp.html#X8-1"

try:
    # Send HTTP GET request with streaming enabled
    with requests.get(url, stream=True, timeout=5) as res:
        res.raise_for_status()

        # Create an incremental parser
        parser = html.HTMLParser()
        tree = None
        t8_rows = []

        # Process the response in chunks
        for chunk in res.iter_content(chunk_size=8192):
            if not chunk:
                continue

            # Feed the chunk to the parser
            if tree is None:
                tree = html.parse(BytesIO(chunk), parser=parser)
            else:
                tree = html.parse(BytesIO(chunk), parser=parser)

            # Find the <a> tag with id="T8-1"
            target_anchor = tree.xpath("//a[@id='T8-1']")
            if not target_anchor:
                continue

            target_anchor = target_anchor[0]  # First matching <a> tag
            # Find the parent <table>
            table = target_anchor.xpath("ancestor::table[1]")
            if not table:
                continue

            table = table[0]  # First parent <table>
            # Extract all rows under this table
            rows = table.xpath(".//tr")
            for row in rows:
                cells = row.xpath(".//td")
                if len(cells) >= 2:  # Ensure the row has at least 2 <td> elements
                    # First <td>: Firmware version (and ILOM version)
                    firmware_version = cells[0].text_content().strip()
                    if firmware_version:
                        t8_rows.append(f"Firmware: {firmware_version}")
                        print(firmware_version)
                    # Second <td>: Download link and date
                    if len(cells) > 1:  # Check if second <td> exists
                        download_info = cells[1].text_content().strip()
                        if download_info:
                            t8_rows.append(f"Download: {download_info}")

            # Stop processing chunks since we found the target section
            break

        # Write the extracted data to a text file
        if t8_rows:
            with open("t8_firmware.txt", "w", buffering=8192) as file:
                file.write("\n".join(t8_rows))
        else:
            print("No rows found in the T8-1 section.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
