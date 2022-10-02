import glob
import json

import pandas as pd

filejson = sorted(glob.glob('tempatjson/*.json'))
datas = []
for i in filejson:
    with open(i) as jsonfile:
        dattt = json.load(jsonfile)
        datas.extend(dattt)

df = pd.DataFrame(datas)
df.to_csv('data img.csv', index=False)
df.to_excel('data img.xlsx', index=False)

with open('data img.json', 'w+') as outfile:
    json.dump(datas, outfile)

print('Done!!')
