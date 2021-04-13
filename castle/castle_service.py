import base64
import requests
import json
import os

from utils.parser import Parser
from kong.kong_service import KongService

class CastleService:

    RISK_THRESHOLD = 0.9
    API_KEY = 'castle_api_key'

    def bot_detection(self, request):
        castle_event_name = self.get_castle_event_name(request)

        if castle_event_name == "":
            print('rejecting request')
            return {
                "status": 405,
                "statusDescription": "Method Not Allowed"
            }

        castle_assessment = self.get_castle_assessment(request, castle_event_name)
        
        risk_score = castle_assessment.get('risk')
        prod_status = "200"

        if risk_score > self.RISK_THRESHOLD or castle_assessment.get('action') == "deny":
            prod_status = "403"

        if castle_assessment.get('action') == "allow":
            return KongService().forward_to_kong(request)
        
        obj = {
            "prod_status": prod_status,
            "risk_score": risk_score,
            "risk_threshold": self.RISK_THRESHOLD,
            "castle_assessment": castle_assessment
        }

        response = Parser.parser_response(obj)

        return response

    def get_castle_event_name(self, request):
        return "$login.attempted"

    def scrubHeaders(self, request_headers):
        scrubbedHeaders = {}
        for header in request_headers:
            headers_to_exclude = ['cookie', 'authorization']

            if header not in headers_to_exclude:
                scrubbedHeaders[header] = request_headers[header][0].get('value')
        
        return scrubbedHeaders

    def castle_auth(self):
        api_key_encoded = base64.b64encode(self.API_KEY.encode()).decode("utf-8")

        return f'Basic {api_key_encoded}'

    def get_castle_assessment(self, request, castle_event_name):
        header = self.scrubHeaders(request.get('headers'))
        auth = self.castle_auth()

        body = {
            "event": castle_event_name,
            "context": {
                "client_id": request.get('client_id'),
                "ip": request.get('clientIp'),
                "headers": header
            }
        }

        headers = {
            "Authorization": auth,
            "Content-Type": "application/json",
            "Content-Length": str(len(body))
        }

        uri = "https://api.castle.io/v1/authenticate"

        response = requests.post(uri, json=body, headers=headers)

        return response.json()
    