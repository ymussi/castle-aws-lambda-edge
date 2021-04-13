
import requests
from utils.parser import Parser

class KongService:

    URL_KONG = 'https://kong.example.com'

    def forward_to_kong(self, request):
        client_id = request.get('client_id')
        kong_params = request.get('kongParams')
        params = self.set_kong_params(client_id, kong_params)

        request = self.send_post(params)

        print(request)

    def set_kong_params(self, client_id, kong_params):
        return Parser.parser_kong_send_params(kong_params)

    def send_post(self, params):
        payload = params.get('payload')
        path = params.get('path')
        headers = params.get('headers')
        uri = self.URL_KONG + "/" + path

        request = requests.post(uri, json=payload, headers=headers)

        return request.json()
