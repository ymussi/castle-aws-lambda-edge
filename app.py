import json

from castle.castle_service import CastleService

def lambda_handler(event, context):
    request = event.get('Records')[0].get('cf').get('request')

    response = CastleService().bot_detection(request)

    return response
