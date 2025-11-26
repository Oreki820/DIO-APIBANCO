from datetime import datetime

# Banco de dados simples em memória
clientes_db = []
contas_db = []
transacoes_db = []


class Cliente:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome


class Conta:
    def __init__(self, id: int, cliente_id: int, saldo: float = 0):
        self.id = id
        self.cliente_id = cliente_id
        self.saldo = saldo


class Transacao:
    def __init__(self, conta_id: int, tipo: str, valor: float):
        self.conta_id = conta_id
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.utcnow()
