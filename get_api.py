import pandas as pd
import numpy as np
#import matplotlib as plotlib

import requests 

# The API endpoint
url = "https://data.enedis.fr/api/explore/v2.0/catalog/exports/csv"

# A get request to the API
response = requests.get(url)

# Print the response
response_json = response.json()

for i in response_json:
    print(i, "\n")