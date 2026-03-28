from fastapi.responses import JSONResponse


def success_response(message: str, download_url: str, file_id: str):
    return JSONResponse({"success": True, "message": message, "file_id": file_id, "download_url": download_url})


def error_response(message: str, status_code: int = 400):
    return JSONResponse({"success": False, "message": message}, status_code=status_code)
