import json
import uuid
from typing import List, Dict, Optional, Union
from urllib.parse import urlparse, parse_qs

from requests import Request as Req, PreparedRequest

from request2postman.headers import DEFAULT_SKIP_HEADERS


class Request:
    def __init__(
        self,
        request: Union[Req, PreparedRequest],
        *,
        name: str = None,
        skip_headers: List[str] = None,
    ):
        if not (isinstance(request, Req) or isinstance(request, PreparedRequest)):
            raise Exception(f"Unsupported request type - {request.__class__}")

        self._request = request if isinstance(request, PreparedRequest) else Req

        self.name = name
        self.skip_headers = (
            DEFAULT_SKIP_HEADERS
            if skip_headers is None
            else [header.lower() for header in skip_headers]
        )
        self._parsed_request = {}

    @property
    def json(self) -> str:
        return json.dumps(self.parsed_request)

    @property
    def parsed_request(self) -> Dict:
        if self._parsed_request:
            return self._parsed_request

        self._parsed_request = self._parse_prepared_request()
        return self._parsed_request

    def _parse_prepared_request(self) -> Dict:
        parsed_url = urlparse(self._request.url)
        parsed_qs = parse_qs(parsed_url.query)
        request_json = {
            "id": str(uuid.uuid4()),
            "name": self.name or self._request.path_url,
            "response": [],
            "event": [],
            "request": {
                "url": {
                    "raw": self._request.url,
                    "protocol": parsed_url.scheme,
                    "path": [path for path in parsed_url.path.split("/") if path],
                    "host": parsed_url.hostname.split("."),
                    "query": [
                        {
                            "key": key,
                            "value": ",".join([str(value) for value in values]),
                        }
                        for key, values in parsed_qs.items()
                    ],
                    "variable": [],
                },
                "header": [
                    {"key": key, "value": value}
                    for key, value in self._request.headers.items()
                    if key.lower() not in self.skip_headers
                ],
                "method": self._request.method,
            },
        }
        if self._request.body:
            request_json["request"]["body"] = self._parse_body()

        return request_json

    def _parse_body(self) -> Optional[Dict]:
        if not self._request.body:
            return
        if self._request.headers["Content-Type"] in ["text/plain", "application/json"]:
            return {
                "mode": "raw",
                "raw": self._request.body.decode("utf-8"),
            }
        elif "multipart/form-data" in self._request.headers["Content-Type"]:
            return {
                "mode": "formdata",
                "formdata": [{"key": "file", "type": "file", "request2postman": []}],
            }
