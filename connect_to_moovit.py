import bs4
import requests
import re
from text_unidecode import unidecode



site = requests.get(
    "https://moovitapp.com/index/en/public_transit-lines-Israel-1-1")
soup = bs4.BeautifulSoup(site.text, 'html.parser')

# Downloading main page and finding links
links2 = soup.select('div[class="lines-container agency-lines"] a[href]')
while (True):
    select = input("Enter bus number (q to quit): ")
    if (select.upper() == "Q"):
        break
    web = ""
    bus = re.compile(r'\d+')
    bus_lines = []
    for i in range(0, len(links2)):
        # Finding link with bus number
        if (bus.search(links2[i].get('href')).group() == select):
            bus_lines.append(links2[i])

    for index, i in enumerate(bus_lines):
        print(index,"--",i.getText().replace('\n',"")[2:])
    bus_line_index = 0
    if len(bus_lines) > 1:
        bus_line_index = input("witch one ? ")

    web = links2[int(bus_line_index)].get('href')

    site = requests.get("https://moovitapp.com/index/en/" + web)
    # Downloading page with bus stops
    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    links = soup.select('ul[class="stops-list bordered"] h3')
    stops = []
    e = 1

    for index in range(0, len(links)):
        print(index,"--",links[index].getText())

    start = input("Enter start station: ")
    end = input("Enter end station: ")

    start_end = links[int(start):int(end)]
    for station in start_end:
        print(station.getText())


