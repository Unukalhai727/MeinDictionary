from datetime import datetime
from pathlib import Path
from tempfile import gettempdir

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from file_hander import processor

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
STORAGE_DIR = Path(gettempdir()) / "MeinDictionary"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse(Path("index.html").read_text(encoding="utf-8"))

@app.get("/files")
async def list_files() -> JSONResponse:
    items = [
        {"name": f.name, "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat()}
        for f in STORAGE_DIR.glob("*") if f.is_file()
    ]
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return JSONResponse({"files": items})

@app.post("/upload")
async def upload(file: UploadFile) -> JSONResponse:
    try:
        assert file.filename, "No file uploaded"
        processed_file, processed_filename = await processor(await file.read(), file.filename)
        with open(STORAGE_DIR / processed_filename, "wb") as f:
            f.write(processed_file)
        return JSONResponse({"stored_as": processed_filename})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download/{filename}")
async def download(filename: str) -> FileResponse:
    return FileResponse(STORAGE_DIR / filename)

@app.delete("/files/{filename}")
async def delete_file(filename: str) -> JSONResponse:
    (STORAGE_DIR / filename).unlink(missing_ok=True)
    return JSONResponse({"deleted": filename})

@app.post("/refresh")
async def refresh_files() -> JSONResponse:
    for path in STORAGE_DIR.glob("*"): path.unlink()
    return JSONResponse({"files": []})
