from fastapi import APIRouter, HTTPException
from app.models import clientes_db, contas_db, transacoes_db, Cliente, Conta, Transacao
from app.schemas import ClienteCreate, ContaCreate, Operacao, Transferencia

router = APIRouter()


# CLIENTES
@router.post("/clientes")
async def criar_cliente(data: ClienteCreate):
    novo_id = len(clientes_db) + 1
    cliente = Cliente(id=novo_id, nome=data.nome)
    clientes_db.append(cliente)
    return {"id": novo_id, "nome": data.nome}


# CONTAS
@router.post("/contas")
async def criar_conta(data: ContaCreate):
    cliente = next((c for c in clientes_db if c.id == data.cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    nova_conta_id = len(contas_db) + 1
    conta = Conta(id=nova_conta_id, cliente_id=data.cliente_id)
    contas_db.append(conta)
    return {"id": nova_conta_id, "cliente_id": conta.cliente_id, "saldo": conta.saldo}


@router.get("/contas/{id}")
async def consultar_conta(id: int):
    conta = next((c for c in contas_db if c.id == id), None)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"id": conta.id, "cliente_id": conta.cliente_id, "saldo": conta.saldo}


# OPERAÇÕES
@router.post("/depositar")
async def depositar(op: Operacao):
    conta = next((c for c in contas_db if c.id == op.conta_id), None)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    conta.saldo += op.valor
    transacoes_db.append(Transacao(conta_id=op.conta_id, tipo="deposito", valor=op.valor))
    return {"saldo": conta.saldo}


@router.post("/sacar")
async def sacar(op: Operacao):
    conta = next((c for c in contas_db if c.id == op.conta_id), None)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if conta.saldo < op.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    conta.saldo -= op.valor
    transacoes_db.append(Transacao(conta_id=op.conta_id, tipo="saque", valor=op.valor))
    return {"saldo": conta.saldo}


@router.post("/transferir")
async def transferir(data: Transferencia):
    origem = next((c for c in contas_db if c.id == data.origem_id), None)
    destino = next((c for c in contas_db if c.id == data.destino_id), None)

    if not origem or not destino:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if origem.saldo < data.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    origem.saldo -= data.valor
    destino.saldo += data.valor

    transacoes_db.append(Transacao(conta_id=origem.id, tipo="transferencia_saida", valor=data.valor))
    transacoes_db.append(Transacao(conta_id=destino.id, tipo="transferencia_entrada", valor=data.valor))

    return {"origem_saldo": origem.saldo, "destino_saldo": destino.saldo}
