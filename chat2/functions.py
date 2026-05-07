"""
Sistema de Funções Registradas
Contém as funções que podem ser executadas pelo agent
"""

from typing import Any, Dict, Callable
from decimal import Decimal


class FunctionRegistry:
    """Registro e gerenciamento de funções disponíveis"""
    
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self._register_default_functions()
    
    def _register_default_functions(self):
        """Registra as funções padrão"""
        self.register("multiplicar", multiplicar)
        self.register("calcular_decimal", calcular_decimal)
        self.register("saudacao", saudacao)
    
    def register(self, name: str, func: Callable):
        """Registra uma nova função"""
        self.functions[name] = func
    
    def get_function(self, name: str) -> Callable:
        """Obtém uma função pelo nome"""
        return self.functions.get(name)
    
    def execute(self, func_name: str, **params) -> Any:
        """Executa uma função registrada"""
        func = self.get_function(func_name)
        if not func:
            raise ValueError(f"Função '{func_name}' não encontrada")
        return func(**params)
    
    def list_functions(self) -> Dict[str, str]:
        """Lista todas as funções disponíveis com suas descrições"""
        return {
            "multiplicar": "Multiplica dois números: multiplicar(a, b)",
            "calcular_decimal": "Arredonda um número para 10 casas decimais: calcular_decimal(valor)",
            "saudacao": "Retorna uma saudação personalizada: saudacao(nome)"
        }


# ============================================================================
# FUNÇÕES MOCK
# ============================================================================

def multiplicar(a: float, b: float) -> float:
    """
    Multiplica dois números
    
    Args:
        a: Primeiro número
        b: Segundo número
    
    Returns:
        Resultado da multiplicação
    """
    return float(a * b)


def calcular_decimal(valor: float) -> float:
    """
    Arredonda um número para 10 casas decimais
    
    Args:
        valor: Número a arredondar
    
    Returns:
        Número arredondado para 10 casas decimais
    """
    return float(Decimal(str(valor)).quantize(Decimal('0.0000000001')))


def saudacao(nome: str) -> str:
    """
    Retorna uma saudação personalizada
    
    Args:
        nome: Nome da pessoa
    
    Returns:
        Mensagem de saudação
    """
    return f"Olá {nome}! 👋 Seja bem-vindo ao nosso assistente!"


# Instância global do registro
registry = FunctionRegistry()
