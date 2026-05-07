"""
Agent com Função de Decisão
Interpreta a intenção do usuário e decide qual função chamar
"""

import re
import time
from typing import Dict, Tuple, Optional, Any
from functions import registry
from logger import logger


class AIAgent:
    """Agent que interpreta intenções e executa functions"""
    
    def __init__(self):
        # Mapping de palavras-chave para funções
        self.intent_keywords = {
            "multiplicar": {
                "keywords": ["multiplicar", "vezes", "produto", "×", "*"],
                "function": "multiplicar",
                "params_pattern": r'(\d+\.?\d*)\s*(?:vezes|×|\*|x)\s*(\d+\.?\d*)',
                "param_names": ["a", "b"]
            },
            "calcular_decimal": {
                "keywords": ["decimal", "arredondar", "casas", "precisão"],
                "function": "calcular_decimal",
                "params_pattern": r'(\d+\.?\d*)',
                "param_names": ["valor"]
            },
            "saudacao": {
                "keywords": ["olá", "oi", "olá", "ola", "nome", "saudação", "apresenta"],
                "function": "saudacao",
                "params_pattern": r"(?:olá|oi|nome)\s+([\w\s]+?)(?:\?|$|\.)",
                "param_names": ["nome"]
            }
        }
    
    def detect_intent(self, user_input: str) -> Optional[str]:
        """
        Detecta a intenção do usuário baseado em palavras-chave
        
        Args:
            user_input: Entrada do usuário
        
        Returns:
            Nome da intenção detectada ou None
        """
        user_input_lower = user_input.lower()
        
        for intent_name, intent_config in self.intent_keywords.items():
            for keyword in intent_config["keywords"]:
                if keyword in user_input_lower:
                    return intent_name
        
        return None
    
    def extract_parameters(
        self,
        user_input: str,
        intent: str
    ) -> Dict[str, Any]:
        """
        Extrai parâmetros da entrada do usuário
        
        Args:
            user_input: Entrada do usuário
            intent: Intenção detectada
        
        Returns:
            Dicionário com os parâmetros extraídos
        """
        intent_config = self.intent_keywords.get(intent, {})
        pattern = intent_config.get("params_pattern")
        param_names = intent_config.get("param_names", [])
        
        if not pattern:
            return {}
        
        match = re.search(pattern, user_input, re.IGNORECASE)
        if not match:
            return {}
        
        params = {}
        for i, param_name in enumerate(param_names):
            try:
                value = match.group(i + 1)
                # Tenta converter para float se possível
                try:
                    params[param_name] = float(value)
                except ValueError:
                    params[param_name] = value
            except IndexError:
                pass
        
        return params
    
    def process_message(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Processa uma mensagem do usuário e retorna a resposta
        
        Args:
            user_input: Entrada do usuário
        
        Returns:
            Tupla (resposta, metadata)
        """
        metadata = {
            "intent": None,
            "function_called": None,
            "parameters": {},
            "result": None,
            "error": None,
            "execution_time_ms": 0
        }
        
        # Log da mensagem do usuário
        logger.log_message("user", user_input)
        
        # Detectar intenção
        intent = self.detect_intent(user_input)
        metadata["intent"] = intent
        
        if not intent:
            response = "❌ Desculpe, não consegui entender sua intenção. Tente mencionar: 'multiplicar', 'decimal' ou 'olá'."
            logger.log_message("assistant", response)
            return response, metadata
        
        # Extrair parâmetros
        params = self.extract_parameters(user_input, intent)
        metadata["parameters"] = params
        
        function_name = self.intent_keywords[intent]["function"]
        metadata["function_called"] = function_name
        
        # Validar parâmetros
        if not params:
            response = f"⚠️ Não consegui extrair os parâmetros necessários. Por favor, forneça números válidos."
            logger.log_message("assistant", response)
            return response, metadata
        
        # Executar função
        try:
            start_time = time.time()
            result = registry.execute(function_name, **params)
            execution_time = (time.time() - start_time) * 1000  # converter para ms
            
            metadata["result"] = result
            metadata["execution_time_ms"] = execution_time
            
            # Log da execução da função
            logger.log_function_call(
                function_name=function_name,
                params=params,
                result=result,
                execution_time_ms=execution_time
            )
            
            # Formatar resposta
            if function_name == "multiplicar":
                response = f"✅ **Resultado:** {params['a']} × {params['b']} = **{result}**\n⏱️ Tempo: {execution_time:.2f}ms"
            elif function_name == "calcular_decimal":
                response = f"✅ **Resultado:** {params['valor']} arredondado para 10 casas = **{result}**\n⏱️ Tempo: {execution_time:.2f}ms"
            elif function_name == "saudacao":
                response = f"✅ {result}\n⏱️ Tempo: {execution_time:.2f}ms"
            else:
                response = f"✅ **Resultado:** {result}\n⏱️ Tempo: {execution_time:.2f}ms"
            
            logger.log_message("assistant", response)
            return response, metadata
        
        except Exception as e:
            error_msg = str(e)
            metadata["error"] = error_msg
            
            # Log do erro
            logger.log_function_call(
                function_name=function_name,
                params=params,
                result=None,
                error=error_msg
            )
            
            response = f"❌ **Erro ao executar função:** {error_msg}"
            logger.log_message("assistant", response)
            return response, metadata
    
    def get_help(self) -> str:
        """Retorna mensagem de ajuda"""
        help_text = """
## 📚 Como usar o Assistente

### Operações Disponíveis:

1. **Multiplicar** 
   - Exemplos: "quanto é 5 vezes 3?", "multiplicar 10 por 7"
   - Palavras-chave: multiplicar, vezes, ×, *

2. **Calcular Decimal**
   - Exemplos: "arredondar 3.14159", "decimal 2.71828"
   - Palavras-chave: decimal, arredondar, casas, precisão

3. **Saudação**
   - Exemplos: "olá João", "oi Maria"
   - Palavras-chave: olá, oi, nome

### 💡 Dicas:
- Seja específico com os números
- Use linguagem natural
- O sistema tentará extrair os parâmetros automaticamente
        """
        return help_text
