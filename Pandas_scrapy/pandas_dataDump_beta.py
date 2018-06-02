import requests
import json
import re
from bs4 import BeautifulSoup
#This is beta version.. in this program i am just fetching all the relevant link fro all methods




method_name='merge'

url = "http://pandas.pydata.org/pandas-docs/stable/api.html"
# print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# print(soup.prettify())

data = response.text
print(data)

soup.title.parent.name
soup.p
soup.p['class']
for link in soup.find_all('a'):
    print(link.get('href'))

soup.a
soup.find_all('a')

soup.find(id="link3")
print(type(data))

pattern = re.compile(r'href="generated/pandas.*\"')
soup = BeautifulSoup(response.text, 'html.parser')
script = re.findall('href="generated/pandas.*?#', response.text, re.IGNORECASE)

print(script)
for i in script:
 print(i.split('href="generated/pandas.'))
