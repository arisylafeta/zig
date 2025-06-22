import os

apollo_config = {
    "apiKey": os.environ.get("APOLLO_API_KEY"),
    "endpoint": "https://api.apollo.io",
}

class ApolloError(Exception):
    def __init__(self, status, body, message=None):
        self.status = status
        self.body = body
        super().__init__(message)
        self.name = "ApolloError"