import json
from os import path

from locust import HttpLocust, TaskSet, task


def is_v1_endpoint(url):
    return url.startswith('/api/v1/')


class RequestExcelFiles(TaskSet):
    endpoints = []
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    def on_start(self):
        with open(path.join(path.dirname(__file__), 'endpoint_urls'), 'r') as endpoints_file:
            self.endpoints = json.load(endpoints_file)

    @task
    def api_v1(self):
        for endpoint in self.endpoints:
            if is_v1_endpoint(endpoint):
                response = self.client.get(endpoint,
                                           headers={'Origin': 'https://www.coordinador.cl',
                                                    'Referer': 'https://www.coordinador.cl/',
                                                    'Accept': self.media_type})
                print(response.content)


class WebsiteUser(HttpLocust):
    task_set = RequestExcelFiles
    min_wait = 0
    max_wait = 3000