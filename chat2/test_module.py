"""
Testes Unitários
Testes para as funções do sistema
"""

import unittest
from .functions import multiplicar, calcular_decimal, saudacao, FunctionRegistry
from .agent import AIAgent
from .logger import Logger


class TestFunctions(unittest.TestCase):
    """Testes das funções utilitárias"""
    
    def test_multiplicar(self):
        """Testa multiplicação"""
        self.assertEqual(multiplicar(5, 3), 15)
        self.assertEqual(multiplicar(10, 2), 20)
        self.assertEqual(multiplicar(0, 100), 0)
        self.assertEqual(multiplicar(-5, 2), -10)
    
    def test_calcular_decimal(self):
        """Testa arredondamento de decimais"""
        result = calcular_decimal(3.14159265359)
        self.assertEqual(result, 3.1415926536)
        
        result2 = calcular_decimal(2.71828182846)
        self.assertEqual(result2, 2.7182818285)
    
    def test_saudacao(self):
        """Testa saudação"""
        self.assertIn("João", saudacao("João"))
        self.assertIn("bem-vindo", saudacao("Python"))


class TestFunctionRegistry(unittest.TestCase):
    """Testes do registro de funções"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.registry = FunctionRegistry()
    
    def test_register_function(self):
        """Testa registro de função"""
        def test_func():
            return "test"
        
        self.registry.register("test", test_func)
        self.assertIsNotNone(self.registry.get_function("test"))
    
    def test_execute_function(self):
        """Testa execução de função"""
        result = self.registry.execute("multiplicar", a=5, b=3)
        self.assertEqual(result, 15)
    
    def test_list_functions(self):
        """Testa listagem de funções"""
        funcs = self.registry.list_functions()
        self.assertIn("multiplicar", funcs)
        self.assertIn("calcular_decimal", funcs)
        self.assertIn("saudacao", funcs)


class TestAIAgent(unittest.TestCase):
    """Testes do AI Agent"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.agent = AIAgent()
    
    def test_intent_detection_multiplicar(self):
        """Testa detecção de multiplicação"""
        intent = self.agent.detect_intent("quanto é 5 vezes 3")
        self.assertEqual(intent, "multiplicar")
        
        intent2 = self.agent.detect_intent("multiplica 10 por 2")
        self.assertEqual(intent2, "multiplicar")
    
    def test_intent_detection_decimal(self):
        """Testa detecção de arredondamento"""
        intent = self.agent.detect_intent("arredondar 3.14")
        self.assertEqual(intent, "calcular_decimal")
    
    def test_intent_detection_saudacao(self):
        """Testa detecção de saudação"""
        intent = self.agent.detect_intent("olá João")
        self.assertEqual(intent, "saudacao")
    
    def test_intent_detection_none(self):
        """Testa detecção quando não há intenção"""
        intent = self.agent.detect_intent("fale sobre Python")
        self.assertIsNone(intent)
    
    def test_parameter_extraction_multiplicar(self):
        """Testa extração de parâmetros para multiplicação"""
        params = self.agent.extract_parameters("5 vezes 3", "multiplicar")
        self.assertEqual(params["a"], 5.0)
        self.assertEqual(params["b"], 3.0)
    
    def test_parameter_extraction_decimal(self):
        """Testa extração de parâmetros para decimal"""
        params = self.agent.extract_parameters("arredondar 3.14159", "calcular_decimal")
        self.assertEqual(params["valor"], 3.14159)
    
    def test_parameter_extraction_saudacao(self):
        """Testa extração de parâmetros para saudação"""
        params = self.agent.extract_parameters("olá João", "saudacao")
        self.assertEqual(params["nome"], "João")
    
    def test_process_message_multiplicar(self):
        """Testa processamento de mensagem de multiplicação"""
        response, metadata = self.agent.process_message("quanto é 5 vezes 3?")
        self.assertEqual(metadata["intent"], "multiplicar")
        self.assertEqual(metadata["result"], 15)
        self.assertIn("15", response)
    
    def test_process_message_invalid(self):
        """Testa processamento de mensagem inválida"""
        response, metadata = self.agent.process_message("fale sobre Python")
        self.assertIsNone(metadata["intent"])
        self.assertIn("não consegui", response.lower())


class TestLogger(unittest.TestCase):
    """Testes do sistema de logging"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.logger = Logger()
    
    def test_log_function_call(self):
        """Testa logging de função"""
        log = self.logger.log_function_call(
            "test_func",
            {"a": 1, "b": 2},
            3
        )
        
        self.assertEqual(log["function"], "test_func")
        self.assertEqual(log["params"], {"a": 1, "b": 2})
        self.assertEqual(log["result"], 3)
        self.assertIsNotNone(log["timestamp"])
    
    def test_log_message(self):
        """Testa logging de mensagem"""
        log = self.logger.log_message("user", "Hello")
        
        self.assertEqual(log["type"], "user")
        self.assertEqual(log["content"], "Hello")
        self.assertIsNotNone(log["timestamp"])
    
    def test_get_all_logs(self):
        """Testa obter todos os logs"""
        self.logger.log_function_call("func1", {}, "result1")
        self.logger.log_message("user", "msg1")
        
        logs = self.logger.get_all_logs()
        self.assertEqual(len(logs), 2)
    
    def test_get_function_logs(self):
        """Testa filtrar logs de funções"""
        self.logger.log_function_call("func1", {}, "result1")
        self.logger.log_message("user", "msg1")
        
        logs = self.logger.get_function_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["function"], "func1")
    
    def test_get_message_logs(self):
        """Testa filtrar logs de mensagens"""
        self.logger.log_function_call("func1", {}, "result1")
        self.logger.log_message("user", "msg1")
        
        logs = self.logger.get_message_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["type"], "user")
    
    def test_clear_logs(self):
        """Testa limpar logs"""
        self.logger.log_function_call("func1", {}, "result1")
        self.logger.clear_logs()
        
        logs = self.logger.get_all_logs()
        self.assertEqual(len(logs), 0)
    
    def test_get_stats(self):
        """Testa obter estatísticas"""
        self.logger.log_function_call("multiplicar", {"a": 5, "b": 3}, 15)
        self.logger.log_function_call("multiplicar", {"a": 2, "b": 2}, 4)
        self.logger.log_message("user", "msg1")
        
        stats = self.logger.get_stats()
        self.assertEqual(stats["total_logs"], 3)
        self.assertEqual(stats["total_function_calls"], 2)
        self.assertEqual(stats["total_messages"], 1)
        self.assertEqual(stats["functions_called"]["multiplicar"], 2)


class TestIntegration(unittest.TestCase):
    """Testes de integração do sistema completo"""
    
    def setUp(self):
        """Setup para cada teste"""
        self.agent = AIAgent()
        self.test_logger = Logger()
    
    def test_full_flow_multiplicar(self):
        """Testa fluxo completo de multiplicação"""
        response, metadata = self.agent.process_message("quanto é 10 vezes 20?")
        
        self.assertIsNotNone(metadata["intent"])
        self.assertIsNotNone(metadata["result"])
        self.assertEqual(metadata["result"], 200)
        self.assertIn("200", response)
    
    def test_full_flow_multiple_messages(self):
        """Testa múltiplas mensagens"""
        messages = [
            "quanto é 5 vezes 3?",
            "arredondar 2.71828",
            "olá Maria"
        ]
        
        results = []
        for msg in messages:
            response, metadata = self.agent.process_message(msg)
            results.append(metadata)
        
        self.assertEqual(len(results), 3)
        self.assertIsNotNone(results[0]["result"])
        self.assertIsNotNone(results[1]["result"])
        self.assertIsNotNone(results[2]["result"])


if __name__ == "__main__":
    unittest.main()
