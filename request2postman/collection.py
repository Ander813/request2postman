import json
import uuid
from typing import List, Union

from requests import PreparedRequest, Request as Req

from request2postman.headers import DEFAULT_SKIP_HEADERS
from request2postman.request import Request


class Collection:
    def __init__(self, name: str, *, skip_headers: List[str] = None):
        self._collection = {
            "info": {
                "_postman_id": str(uuid.uuid4()),
                "name": name,
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            },
            "event": [],
            "variable": [],
            "item": [],
        }
        self.skip_headers = (
            DEFAULT_SKIP_HEADERS
            if skip_headers is None
            else [header.lower() for header in skip_headers]
        )

    def add_variable(self, key: str, value: str):
        variable = [
            variable
            for variable in self._collection["variable"]
            if variable["id"] == key
        ]
        if variable:
            variable[0]["value"] = value
        else:
            self._collection["variable"].append(
                {"id": key, "value": value, "type": "string"}
            )

    def describe(self, description: str, type_: str = "text/plain"):
        self._collection["info"]["description"] = {
            "content": description,
            "type": type_,
        }

    def add_request(
        self, request: Union[PreparedRequest, Req, Request], name: str = None
    ):
        if not isinstance(request, Request):
            request = Request(request, name=name, skip_headers=self.skip_headers)
        self._collection["item"].append(request.parsed_request)

    @property
    def json(self) -> str:
        return json.dumps(self._collection)
