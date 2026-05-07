from fastapi import FastAPI
from fastapi.responses import FileResponse 
from fastapi import Request, HTTPException
import os 




app = FastAPI()

@app.get("/files/{file_id}")
def get_file(file_id: str):
    file_path = f"arquivos/{file_id}.pdf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(
        path=file_path,
        filename=f"{file_id}.pdf",
        media_type="application/pdf"
    )

def download_url(params):
    file_id = params.get("file_id")
    if not file_id:
        return {"erro": "file_id não informado"}
    url = f"http://app_arquivo:8000/files/{file_id}"
    return {"url": url}

methods ={
    "download_url": download_url
} 


@app.post("/rpc")
async def rpc(request: Request):
    data = await request.json()
    method_name = data.get("method")
    req_id = data.get("id")
    params = data.get("params",{})

    method = methods.get(method_name)
    if not method:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": req_id
        }

    try:
        result = method(params)
        return{
            "jsonrpc":"2.0",
            "result": result,
            "id": req_id
        }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": str(e)},
            "id": req_id
        }