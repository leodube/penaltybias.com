from .views import Home, PenaltyApi

def initialize_urls(api):
  api.add_resource(PenaltyApi, '/api/predict-penalties')
  api.add_resource(Home, '/')