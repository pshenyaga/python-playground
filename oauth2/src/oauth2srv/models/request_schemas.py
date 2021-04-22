from webargs import fields, validate

authorize_schema = {
    'argmap': {
        'client_id': fields.String(required=True),
        'redirect_uri': fields.URL(required=True),
        'response_type': fields.String(
            validate=validate.OneOf(["code"]), required=True),
        'state': fields.String(required=False)
    },
    'location': 'query'
}

approve_schema = {
    'argmap': {
        'reqid': fields.String(required=True),
        'approve': fields.String(required=True)
    },
    'location': 'form'
}

token_schema_headers = {
    'argmap': {
        'authorization': fields.String(required=False)
    },
    'location': 'headers'
}

token_schema_json = {
    'argmap': {
        'grant_type': fields.String(
            validate=validate.OneOf(['authorization_code']), required=True),
        'code': fields.String(required=False),
        'client_id': fields.String(required=False),
        'client_secret': fields.String(required=False),
        'redirect_uri': fields.URL(required=False)
    },
    'location': 'json'
}