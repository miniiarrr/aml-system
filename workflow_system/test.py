import requests
import json

url = "https://docs-demo.quiknode.pro/"

payload = json.dumps({
  "method": "eth_getTransactionByHash",
  "params": [
    "0xb61413c495fdad6114a7aa863a00b2e3c28945979a10885b12b30316ea9f072c"
  ],
  "id": 1,
  "jsonrpc": "2.0"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
