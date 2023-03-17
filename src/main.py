import os
import requests
from bs4 import BeautifulSoup
import re
import json


class WebParser:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.numbers = []

    def crawl(self):
        response = requests.get(self.url)

        # Check if the request was successful
        if response.status_code == 200:
            print("Crawling the URL...")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links with .json extension
            json_links = soup.find_all('a', href=re.compile(r'\.json'))

            # Ensure the data folder exists
            if not os.path.exists('data'):
                os.makedirs('data')

            print("Writing .json links to 'data/links.txt'...")
            with open("data/links.txt", "w") as output_file:
                for link in json_links:
                    json_url = f"{self.url}/{link['href']}"
                    output_file.write(json_url + "\n")

            print("Links have been written to 'data/links.txt'.")
            self.links = [link['href'] for link in json_links]
        else:
            print("Error: Failed to retrieve the webpage.")
            return False

        return True

    def parse_links(self):
        print("Parsing 'data/links.txt' and extracting filenames without the .json extension...")

        # Use regex to find filenames with only numbers before .json
        pattern = re.compile(r'^\d+\.json')

        # Extract numbers without the .json extension
        for link in self.links:
            filename = link.strip().split('/')[-1]
            match = pattern.search(filename)
            if match:
                number = match.group().replace('.json', '')
                self.numbers.append(number)

        print("Writing extracted numbers to 'data/numbers.json' in JSON format...")
        # Convert the numbers to a JSON format
        json_data = [{"token_id": number} for number in self.numbers]

        with open("data/numbers.json", "w") as output_file:
            json.dump(json_data, output_file, indent=2)

        print("Numbers have been written to 'data/numbers.json'.")


if __name__ == "__main__":
    url = "https://bafybeicoln5rvccttgypzo26irjlskslnfynkzig6bowpsj6ay45geeice.ipfs.nftstorage.link"
    parser = WebParser(url)

    if parser.crawl():
        parser.parse_links()
