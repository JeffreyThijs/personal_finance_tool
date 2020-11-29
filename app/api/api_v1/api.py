from fastapi_utils.inferring_router import InferringRouter

from app.api.api_v1.endpoints.transactions import transactions

api_router = InferringRouter()
api_router.include_router(transactions.router)
