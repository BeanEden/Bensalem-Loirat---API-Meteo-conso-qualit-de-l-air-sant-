import pandas as pd
import numpy as np
#import matplotlib as plotlib
import os
import requests 

# The API endpoint
url = "https://www.data.gouv.fr/fr/datasets/etat-du-trafic-en-temps-reel/#/resources/02666160-4137-4c9a-a859-ed0a9e84679a"

response = requests.get(url)

#print(response.json())
#for i in response_json:
    #print(i, "\n")

df = pd.DataFrame(response)
print(df.head(5))

df.to_csv("test.csv")