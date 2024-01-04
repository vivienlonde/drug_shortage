import requests
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

r = requests.get('https://ansm.sante.fr/disponibilites-des-produits-de-sante/medicaments',
                 verify=False)
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find("table")

danger_list = []

for i, e in enumerate(table.contents[3]):
    if e.name=='tr':
        # print(e, '\n')
        data_href = e["data-href"]
        for f in e:
            if f.name=='td':
                myclass = f.get('class')
                if myclass and 'text-danger' in myclass: 
                    # print(f)
                    danger_list.append(data_href)

for href in danger_list[:5]:
    print(href)
                




# print(type(table.contents[3]))
# line = table.contents[3][1]
# print(line)
