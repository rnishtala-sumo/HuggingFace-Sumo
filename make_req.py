#%%
import requests
import json
#%%
# url = "http://127.0.0.1:5000/" # for flask
url = "http://localhost:9000/" # for docker if exposed to 9000
data = ["Hello, my name is John Doe. I live at 123 Apple Road, New York, NY 10001, and my phone number is (123) 456-7890. I work for Tech Corp. and my email address is john.doe@techcorp.com."]
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)
# %%
# r
# %%
# sent_score = json.loads(r.text)
# sent_score
# %%
# label = sent_score[0]["label"]
# score = sent_score[0]["score"]
# label, score
# %%
