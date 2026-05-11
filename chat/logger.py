"""
Sistema de Logging
Armazena e gerencia logs de execução do agent
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class Logger:
    """Sistema de logging centralizado"""
    
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
    
    def log_function_call(
        self,
        function_name: str,
        params: Dict[str, Any],
        result: Any,
        error: Optional[str] = None,
        execution_time_ms: float = 0
    ) -> Dict[str, Any]:
        """
        Registra uma chamada de função
        """
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "function": function_name,
            "params": params,
            "result": result,
            "error": error,
            "execution_time_ms": execution_time_ms
        }
        self.logs.append(log_entry)
        return log_entry
    
    def log_message(
        self,
        message_type: str,
        content: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Registra uma mensagem de interação
        """
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": message_type,
            "content": content,
            "user_id": user_id
        }
        self.logs.append(log_entry)
        return log_entry
    
    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Retorna todos os logs registrados"""
        return self.logs
    
    def get_function_logs(self) -> List[Dict[str, Any]]:
        """Retorna apenas logs de execução de funções"""
        return [log for log in self.logs if "function" in log]
    
    def get_message_logs(self) -> List[Dict[str, Any]]:
        """Retorna apenas logs de mensagens"""
        return [log for log in self.logs if "type" in log]
    
    def clear_logs(self):
        """Limpa todos os logs"""
        self.logs.clear()
    
    def export_logs_json(self) -> str:
        """Exporta os logs em formato JSON"""
        return json.dumps(self.logs, indent=2, ensure_ascii=False)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas sobre os logs"""
        function_logs = self.get_function_logs()
        
        stats = {
            "total_logs": len(self.logs),
            "total_function_calls": len(function_logs),
            "total_messages": len(self.get_message_logs()),
            "functions_called": {},
            "errors": 0
        }
        
        # Contar funções chamadas e erros
        for log in function_logs:
            func_name = log.get("function")
            if func_name:
                stats["functions_called"][func_name] = stats["functions_called"].get(func_name, 0) + 1
            if log.get("error"):
                stats["errors"] += 1
        
        return stats


# Instância global do logger
logger = Logger()
