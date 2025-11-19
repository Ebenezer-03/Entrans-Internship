from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import predict, stats

app = FastAPI(
    title="King County House Price Prediction API",
    description="API for predicting house prices in King County, WA",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(predict.router, prefix="/api", tags=["prediction"])
app.include_router(stats.router, prefix="/api", tags=["statistics"])

@app.get('/health')
async def health_check():
    return {'status': 'healthy', 'message': 'API is running successfully'}

@app.get('/')
async def root():
    return {
        'message': 'King County House Price Prediction API', 
        'docs': '/docs',
        'health_check': '/health'
    }