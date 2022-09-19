# request2postman
___
Small lib that allows you to automatically 
generate postman collections out of python requests lib
### Using requests hooks
```python
from request2postman import Collection, request_to_postman_hook
from requests import Session


collection = Collection("some_name")
with Session() as session:
    session.hooks["response"].append(request_to_postman_hook(collection))
    session.get("https://httpbin.org/basic-auth/user/pass")
    session.post("https://httpbin.org/basic-auth/user/pass", json={"key": "value"})

with open("collection.json", "w") as file:
    file.write(collection.json)
```
### Using Request object directly
```python
from request2postman import Collection
import requests


resp1 = requests.get("https://httpbin.org/basic-auth/user/pass")
resp2 = requests.post("https://httpbin.org/basic-auth/user/pass", json={"key": "value"})

collection = Collection("some_name")
collection.add_request(resp1.request, name="request1")
collection.add_request(resp2.request)

with open("collection.json", "w") as file:
    file.write(collection.json)
```

Result
```json
{
  "info": {
    "_postman_id": "6fde81f7-6cb8-4cde-bf89-a2b476ed794f",
    "name": "some_name",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "event": [],
  "variable": [],
  "item": [
    {
      "id": "79731ba3-25e5-4149-a975-20c4e7929728",
      "name": "request1",
      "response": [],
      "event": [],
      "request": {
        "url": {
          "raw": "https://httpbin.org/basic-auth/user/pass",
          "protocol": "https",
          "path": [
            "basic-auth",
            "user",
            "pass"
          ],
          "host": [
            "httpbin",
            "org"
          ],
          "query": [],
          "variable": []
        },
        "header": [],
        "method": "GET"
      }
    },
    {
      "id": "0a75dc4e-16ef-468e-a903-412832fd5749",
      "name": "/basic-auth/user/pass",
      "response": [],
      "event": [],
      "request": {
        "url": {
          "raw": "https://httpbin.org/basic-auth/user/pass",
          "protocol": "https",
          "path": [
            "basic-auth",
            "user",
            "pass"
          ],
          "host": [
            "httpbin",
            "org"
          ],
          "query": [],
          "variable": []
        },
        "header": [
          {
            "key": "Content-Length",
            "value": "16"
          },
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "method": "POST",
        "body": {
          "mode": "raw",
          "raw": "{\"key\": \"value\"}"
        }
      }
    }
  ]
}
```
___
#### You can skip some headers to avoid posting Authorization headers or any other private headers with others
```python
from request2postman import Collection
import requests


collection = Collection("some_name", skip_headers=["Authorization"])
resp1 = requests.get("https://httpbin.org/basic-auth/user/pass")
resp2 = requests.post("https://httpbin.org/basic-auth/user/pass", json={"key": "value"})
collection.add_request(resp1.request)
collection.add_request(resp2.request)

with open("collection.json", "w") as file:
    file.write(collection.json)
```