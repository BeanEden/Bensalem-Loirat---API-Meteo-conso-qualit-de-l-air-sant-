import pandas as pd
import numpy as np
#import matplotlib as plotlib
import os
import requests 

# The API endpoint
#url = "https://data.enedis.fr/api/explore/v2.0/catalog/exports/csv"

#url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
#url = "api-portal.electricitymaps.com/v3/carbon-intensity/latest"


#url = "https://public-api.meteofrance.fr/public/DPClim/liste-stations/horaire"
url = "https://public-api.meteofrance.fr/public/DPClim/v1/liste-stations/infrahoraire-6m?id-departement=1"

import os
#from dotenv import load_dotenv

#load_dotenv()
ressource = "/liste-stations/infrahoraire-6m"
base = "https://public-api.meteofrance.fr/public/DPClim/v1"
# A get request to the API
api_key = "eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJKZWFuY29yZW50aW5sb2lyYXRAY2FyYm9uLnN1cGVyIiwiYXBwbGljYXRpb24iOnsib3duZXIiOiJKZWFuY29yZW50aW5sb2lyYXQiLCJ0aWVyUXVvdGFUeXBlIjpudWxsLCJ0aWVyIjoiVW5saW1pdGVkIiwibmFtZSI6IkRlZmF1bHRBcHBsaWNhdGlvbiIsImlkIjoxOTQ0NywidXVpZCI6ImM2MjE5ZmE3LTE5OGEtNGYyMC05YTRjLTMwOGRmYmJiNTc0NCJ9LCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnI6NDQzXC9vYXV0aDJcL3Rva2VuIiwidGllckluZm8iOnsiNTBQZXJNaW4iOnsidGllclF1b3RhVHlwZSI6InJlcXVlc3RDb3VudCIsImdyYXBoUUxNYXhDb21wbGV4aXR5IjowLCJncmFwaFFMTWF4RGVwdGgiOjAsInN0b3BPblF1b3RhUmVhY2giOnRydWUsInNwaWtlQXJyZXN0TGltaXQiOjAsInNwaWtlQXJyZXN0VW5pdCI6InNlYyJ9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJEb25uZWVzUHVibGlxdWVzQ2xpbWF0b2xvZ2llIiwiY29udGV4dCI6IlwvcHVibGljXC9EUENsaW1cL3YxIiwicHVibGlzaGVyIjoiYWRtaW5fbWYiLCJ2ZXJzaW9uIjoidjEiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifV0sImV4cCI6MTgyNDQzMDE3NywidG9rZW5fdHlwZSI6ImFwaUtleSIsImlhdCI6MTcyOTc1NzM3NywianRpIjoiYTNlYzc0MWMtNDI0MC00ZjE5LWI4MTItYWQ4NDEzYWQ3Mjc4In0=.P3B843-QaK3DFRA_lSPnDWl5T_fGb8L0UPcJEyp05mxDxRwNpPCApIMQ-xkhFUHAIh7HlZ7sXtnFV0MRVuz3PLmryJKnAMWkvQhgdpBACcyTC4zLx_RrPMdx7ZiVxwWdvhFDvkvbjBgOgeSJLjP6Ek8PSPTEfVvoccE0o7_HjHaeLOKVIFFZPeo_m8hgGMhnx7wVHIMl4dGoPbJXriqsfMNT1YmVr2KRaO-RV7n5gLgrk7MwijFWsVeLPgB1vDHLhYGzB_xb361XTpsg3KG5Bmv5jkFg4RJSuN1bIwGx485Vr_LDkHiE50rvxboya0LDrfwZNttfjTt7b0mr79llCw=="
url = f"{base}{ressource}&apikey={api_key}"

url = f"https://public-api.meteofrance.fr/public/DPClim/"

response = requests.get(url)

print(response.json())
#for i in response_json:
    #print(i, "\n")

#df = pd.DataFrame(response.json())


