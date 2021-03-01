from .views import PenaltyApi

def initialize_urls(api):
  api.add_resource(PenaltyApi, '/api/predict-penalties')