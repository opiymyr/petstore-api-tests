import time
import json
import pprint
import allure
import requests


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _url(self, endpoint, endpoint_id=None):
        if endpoint_id is None:
            return f"{self.base_url}/{endpoint}"
        return f"{self.base_url}/{endpoint}/{endpoint_id}"

    def send(self, method, endpoint, endpoint_id=None, expected_status=200, retries=1, **kwargs):
        url = self._url(endpoint, endpoint_id)
        with allure.step(f"{method} {url}"):
            if kwargs.get("json") is not None:
                allure.attach(json.dumps(kwargs["json"], indent=2, ensure_ascii=False),
                              name="Тело запроса",
                              attachment_type=allure.attachment_type.JSON)
            response = None
            for attempt in range(retries):
                response = requests.request(method, url, timeout=10, **kwargs)
                if response.status_code == expected_status:
                    break
                if attempt < retries - 1:
                    time.sleep(1)

            allure.attach(f"{response.status_code} {response.reason}\n\n{response.text}",
                          name="Ответ сервера",
                          attachment_type=allure.attachment_type.TEXT)
            pprint.pprint(f"{method} {response.url} -> {response.status_code}")
            return response

    def get(self, endpoint, endpoint_id=None, expected_status=200, params=None):
        return self.send("GET", endpoint, endpoint_id, expected_status, retries=5, params=params)

    def post(self, endpoint, body=None, endpoint_id=None, **kwargs):
        return self.send("POST", endpoint, endpoint_id, json=body, **kwargs)

    def put(self, endpoint, body=None, endpoint_id=None):
        return self.send("PUT", endpoint, endpoint_id, json=body)

    def delete(self, endpoint, endpoint_id):
        return self.send("DELETE", endpoint, endpoint_id)


base_request = BaseRequest("https://petstore.swagger.io/v2")
