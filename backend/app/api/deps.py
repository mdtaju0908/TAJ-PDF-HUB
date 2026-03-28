from fastapi import Depends
from app.core.security import verify_api_key_dependency

# Expose as reusable dependency for routers
verify_api_key = Depends(verify_api_key_dependency)

