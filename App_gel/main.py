from fastapi import FastAPI
import httpx
import gel
import os
from fastapi import Request
from pydantic import BaseModel
from decimal import Decimal

class  ItemNota(BaseModel):
    cpf: str
    id: int

class ItemArea(BaseModel):
    method: str
    nomeArea: str
    id: int

class NovoEmpregado(BaseModel):
    cpf: str
    nome: str
    senha: str
    telefone: list[str]
    rua: str
    cep: str
    numero: int
    matricula: str


class NovaArea(BaseModel):
    nomeArea: str
    cpfGerente: str


class NovoProduto(BaseModel):
    nomeProduto: str
    areas: list[str]

class CriarNota(BaseModel):
    cpfEmpregado: str

class InserirItem(BaseModel):
    idNota: str  
    produto: str
    qtd: int
    preco: Decimal


app = FastAPI()
dsn = os.getenv("GEL_DSN")
if dsn:
    client = gel.create_async_client(dsn=dsn)



@app.get("/baixar/{file_id}")
def baixar_arquivo(file_id:str):
    try:
        rpc_payload ={
            "jsonrpc": "2.0",
            "method": "download_url",
            "params": {"file_id": file_id },
            "id": 1
        }
        try:
            rpc_response = httpx.post(
                "http://app_arquivo:8000/rpc",
                json=rpc_payload
            )
        except Exception as e:
            return {"erro": f"Erro ao chamar RPC: {str(e)}"}
        rpc_data = rpc_response.json()

        if "error" in rpc_data:
            return {"erro": rpc_data["error"]}
        url = rpc_data["result"]["url"]
        file_name = f"downloads/{file_id}.pdf"
        with httpx.stream("GET", url) as response:
            if response.status_code != 200:
                return {"erro": "Falha ao baixar arquivo"}                
        return FileResponse(
            path=file_name,
            filename=f"{file_id}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        return {"erro": str(e)}

@app.get("/Gerentes")
async def listar_gerentes():
    users = await client.query("select Gerente { cpfPessoa, nomePessoa };")
    return users

@app.get("/Empregados")
async def listar_empredos():
    users = await client.query("select Empregado {cpfPessoa,nomePessoa};")
    return users

@app.get("/Area")
async def listar_Area():
    users = await client.query("select Area{nomeArea};")
    return users


@app.post("/NotaFiscal")
async def Listar_notas(item: ItemNota):
    item_dict = item.model_dump()
    try:
        req_cpf = item.cpf
        req_id = item.id
        users = await client.query("select NotaFiscal{empregado:{cpfPessoa,nomePessoa}, data, itens:{produto:{nomeProduto},qtdVenda,precoUnid,subTotal := (.qtdVenda * .precoUnid)}} filter (.empregado.cpfPessoa = <str>$cpf);",cpf=req_cpf)
        return {
            "result": users,
            "id": req_id
        } 
    except Exception as e:
        return {
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }

async def Pega_Produtos(params):
    users = await client.query("select Produto {nomeProduto, areas:{nomeArea}} filter(.areas.nomeArea = <str>$area);",area=params)
    return users

async def Pega_Gerente(params):
    users = await client.query("select Area{gerente:{cpfPessoa,nomePessoa}} filter(.nomeArea = <str>$area);",area=params)
    return users

methods={
    "Pega_Produtos":Pega_Produtos,
    "Pega_Gerente": Pega_Gerente
}

@app.post("/Info_Area")
async def infoArea(item:ItemArea):
    item_dict = item.model_dump()
    try:
        req_method = item.method
        req_Area = item.nomeArea
        req_id = item.id
        method = methods.get(req_method)
        try:
            result= await method(req_Area)
            return{
                "result": result,
                "id": req_id
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": str(e)},
                "id": req_id
            }
    except Exception as e:
        return {
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }


@app.post("/Empregado")
async def criar_empregado(emp: NovoEmpregado):
    try:
        await client.query("""
            insert Empregado {
                cpfPessoa := <str>$cpf,
                nomePessoa := <str>$nome,
                senhaPessoa := <str>$senha,
                telefone := (
                    select array_unpack(<array<str>>$telefone)
                ),
                matriculaEmpregador := <str>$matricula,
                endereco := (
                    insert Endereco {
                        rua := <str>$rua,
                        cep := <str>$cep,
                        numero := <int16>$numero
                    }
                )
            }
        """,
        cpf=emp.cpf,
        nome=emp.nome,
        senha=emp.senha,
        telefone=emp.telefone,
        matricula=emp.matricula,
        rua=emp.rua,
        cep=emp.cep,
        numero=emp.numero
        )

        return {"msg": "Empregado criado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}





@app.post("/Area")
async def criar_area(area: NovaArea):
    try:
        await client.query("""
            insert Area {
                nomeArea := <str>$nome,
                gerente := (
                    select Gerente
                    filter .cpfPessoa = <str>$cpf
                )
            }
        """, nome=area.nomeArea, cpf=area.cpfGerente)

        return {"msg": "Área criada com sucesso"}

    except Exception as e:
        return {"erro": str(e)}


@app.post("/Produto")
async def criar_produto(prod: NovoProduto):
    try:
        await client.query("""
            insert Produto {
                nomeProduto := <str>$nome,
                areas := (
                    select Area
                    filter .nomeArea in array_unpack(<array<str>>$areas)
                )
            }
        """, nome=prod.nomeProduto, areas=prod.areas)

        return {"msg": "Produto criado com sucesso"}

    except Exception as e:
        return {"erro": str(e)}



@app.post("/CriarNota")
async def criar_nota(nota: CriarNota):
    try:
        result = await client.query("""
            insert NotaFiscal {
                empregado := (
                    select Empregado
                    filter .cpfPessoa = <str>$cpf
                ),
                data := cal::to_local_date(datetime_current(), "America/Sao_Paulo")
            }
        """, cpf=nota.cpfEmpregado)

        return {
            "msg": "Nota criada",
            "nota": result
        }

    except Exception as e:
        return {"erro": str(e)}


@app.post("/AdicionarItem")
async def adicionar_item(item: InserirItem):
    try:
        await client.query("""
            update NotaFiscal
            filter .id = <uuid>$idNota
            set {
                itens += (
                    insert ItemNota {
                        produto := assert_single(
                            select Produto
                            filter .nomeProduto = <str>$produto
                        ),
                        qtdVenda := <int16>$qtd,
                        precoUnid := <decimal>$preco
                    }
                )
            }
        """,
        idNota=item.idNota,
        produto=item.produto,
        qtd=item.qtd,
        preco=item.preco
        )

        return {"msg": "Item adicionado"}

    except Exception as e:
        return {"erro": str(e)}