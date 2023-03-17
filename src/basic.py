

import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://bafybeicoln5rvccttgypzo26irjlskslnfynkzig6bowpsj6ay45geeice.ipfs.nftstorage.link"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Crawling the URL...")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links with .json extension
    json_links = soup.find_all('a', href=re.compile(r'\.json'))

    print("Writing .json links to 'links.txt'...")
    with open("links.txt", "w") as output_file:
        for link in json_links:
            json_url = f"{url}/{link['href']}"
            output_file.write(json_url + "\n")

    print("Links have been written to 'links.txt'.")

    print("Parsing 'links.txt' and extracting filenames without the .json extension...")
    with open("links.txt", "r") as input_file:
        links = input_file.readlines()

    # Use regex to find filenames with only numbers before .json
    pattern = re.compile(r'^\d+\.json')

    # Extract numbers without the .json extension
    numbers = []
    for link in links:
        filename = link.strip().split('/')[-1]
        match = pattern.search(filename)
        if match:
            number = match.group().replace('.json', '')
            numbers.append(number)

    print("Writing extracted numbers to 'numbers.json' in JSON format...")
    # Convert the numbers to a JSON format
    json_data = [{"token_id": number} for number in numbers]

    with open("numbers.json", "w") as output_file:
        json.dump(json_data, output_file, indent=2)

    print("Numbers have been written to 'numbers.json'.")
else:
    print("Error: Failed to retrieve the webpage.")
