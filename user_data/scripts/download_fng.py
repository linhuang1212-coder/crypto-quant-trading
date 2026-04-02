import urllib.request
import json
import csv
from datetime import datetime

url = "https://api.alternative.me/fng/?limit=2500"
req = urllib.request.Request(url, headers={'User-Agent': 'FreqtradeBot/1.0'})
r = urllib.request.urlopen(req, timeout=15)
data = json.load(r)

records = data['data']
print(f"Total records: {len(records)}")
print(f"Oldest: {records[-1]}")
print(f"Newest: {records[0]}")

out_path = "/freqtrade/user_data/fng_history.csv" if __name__ != '__main__' else "user_data/fng_history.csv"
with open("user_data/fng_history.csv", 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['date', 'fng_value', 'fng_label'])
    for rec in reversed(records):
        dt = datetime.utcfromtimestamp(int(rec['timestamp'])).strftime('%Y-%m-%d')
        w.writerow([dt, rec['value'], rec['value_classification']])

print(f"Saved to user_data/fng_history.csv")
