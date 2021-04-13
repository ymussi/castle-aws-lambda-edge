import json

class Parser:

    @classmethod
    def parser_response(cls, data):
        return {
            "status": "200",
            "statusDescription": "OK",
            "headers": {
            "cache-control": [{
                "key": "Cache-Control",
                "value": "max-age=100"
            }],
            "content-type": [{
                "key": "Content-Type",
                "value": "application/json"
            }],
            "access-control-allow-origin": [{
                "key": "Access-Control-Allow-Origin",
                "value": "*"
            }],
            "access-control-allow-methods": [{
                "key": "Access-Control-Allow-Methods",
                "value": "GET, HEAD, OPTIONS, POST"
            }]
            },
            "body": json.dumps(data)
        };

    @classmethod
    def parser_kong_send_params(cls, params):
        endpoint = params.get('path').replace("/", "")
        parameters = {
            "verify": {
                "payload": {
                    "login": params.get('login'),
                    "password": params.get('password'),
                    "sessionId": params.get('sessionId')
                },
                "headers": {
                    "authorization": params.get('authorization'),
                    "Content-Type": "application/json",
                },
                "path": "path_kong"
            },
            "login": {
                "payload": {
                    "username": params.get('username'),
                    "password": params.get('password')
                },
                "headers": {
                    "apikey": params.get('apikey'),
                    "Content-Type": "application/json",
                },
                "path": "path_kong"
            }
        }

        return parameters[endpoint]
