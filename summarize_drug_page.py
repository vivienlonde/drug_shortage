import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# href = '/disponibilites-des-produits-de-sante/medicaments/methotrexate-viatris-100-mg-ml-solution-injectable-flacons-de-10-ml-et-50-ml-methotrexate'
href = '/disponibilites-des-produits-de-sante/medicaments/folinate-de-calcium-ebewe-10-mg-ml-solution-injectable-pour-perfusion-folinate-de-calcium'
url = 'https://ansm.sante.fr' + href

r = requests.get(url, verify=False)
soup = BeautifulSoup(r.content, 'html.parser')

mytag = soup.find("div", {"class": "panel-body"})
observations = mytag.text.strip()
print(observations)
# observations = "le médicament est en rupture de stock jusqu'au 31/12/2024."

prompt = '''A partir des informations suivantes,
quand le médicament sera-t-il à nouveau disponible?

Information: {}'''.format(observations)
# prompt += "Dates de disponibilité:"
# print(prompt)

load_dotenv()  

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-05-15"
)

response = client.chat.completions.create(
    model = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    messages=[
        {"role": "system", "content": '''
Tu dois donner les dates de disponibilité de toutes les versions du médicament.
Réponds en listant TOUTES les versions du médicament et leur date de disponibilité.
Réponds de façon extrêmement concise et précise.
Réponds en utilisant le moins de mots possible.
Réponds 'date de disponibilité inconnue' si la date de disponibilité est inconnue.
         
Ne mentionne pas d'autre information que la date de disponibilité.
Ne mentionne surtout pas les interdictions de vente et d'exportation.
'''},
        {"role": "user", "content": prompt}
    ]
)

# print(response.choices[0].message.content)


# EXEMPLE 1:
# Information: le médicament est en rupture de stock jusqu'au 31/12/2024.
# Data de disponibilité: 31/12/2024.

# EXEMPLE 2:
# Information: Pas de date de disponibilité connue.
# Data de disponibilité: NA.