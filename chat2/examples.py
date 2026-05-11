"""
Exemplos de Uso e Testes
Demonstra como usar os componentes do sistema
"""

from .agent import AIAgent
from .functions import registry
from .logger import logger


def exemplo_1_basico():
    """Exemplo básico: Multiplicação"""
    print("=" * 60)
    print("EXEMPLO 1: Multiplicação Básica")
    print("=" * 60)
    
    agent = AIAgent()
    
    # Simular entrada do usuário
    user_input = "Quanto é 5 vezes 3?"
    
    print(f"\n👤 Usuário: {user_input}")
    
    # Processar mensagem
    response, metadata = agent.process_message(user_input)
    
    print(f"\n🤖 Agent: {response}")
    print(f"\n📊 Metadata:")
    print(f"  - Intenção: {metadata['intent']}")
    print(f"  - Função: {metadata['function_called']}")
    print(f"  - Parâmetros: {metadata['parameters']}")
    print(f"  - Resultado: {metadata['result']}")
    print(f"  - Tempo: {metadata['execution_time_ms']:.2f}ms")


def exemplo_2_arredondamento():
    """Exemplo 2: Arredondamento de decimais"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Arredondamento de Decimais")
    print("=" * 60)
    
    agent = AIAgent()
    user_input = "Arredondar 3.14159265359"
    
    print(f"\n👤 Usuário: {user_input}")
    
    response, metadata = agent.process_message(user_input)
    
    print(f"\n🤖 Agent: {response}")
    print(f"\n📊 Metadata:")
    print(f"  - Intenção: {metadata['intent']}")
    print(f"  - Função: {metadata['function_called']}")
    print(f"  - Parâmetros: {metadata['parameters']}")
    print(f"  - Resultado: {metadata['result']}")


def exemplo_3_saudacao():
    """Exemplo 3: Saudação com nome"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Saudação Personalizada")
    print("=" * 60)
    
    agent = AIAgent()
    user_input = "Olá João Silva"
    
    print(f"\n👤 Usuário: {user_input}")
    
    response, metadata = agent.process_message(user_input)
    
    print(f"\n🤖 Agent: {response}")
    print(f"\n📊 Metadata:")
    print(f"  - Intenção: {metadata['intent']}")
    print(f"  - Função: {metadata['function_called']}")
    print(f"  - Parâmetros: {metadata['parameters']}")


def exemplo_4_entradas_invalidas():
    """Exemplo 4: Tratamento de entradas inválidas"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Tratamento de Erros")
    print("=" * 60)
    
    agent = AIAgent()
    
    # Entrada sem intenção clara
    user_input1 = "Como você está?"
    print(f"\n👤 Usuário: {user_input1}")
    response1, _ = agent.process_message(user_input1)
    print(f"🤖 Agent: {response1}")
    
    # Entrada sem parâmetros
    user_input2 = "Multiplicar sem números"
    print(f"\n👤 Usuário: {user_input2}")
    response2, _ = agent.process_message(user_input2)
    print(f"🤖 Agent: {response2}")


def exemplo_5_logging():
    """Exemplo 5: Visualizar logs"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Visualizar Logs")
    print("=" * 60)
    
    agent = AIAgent()
    
    # Executar algumas operações
    inputs = [
        "Quanto é 10 vezes 20?",
        "Arredondar 2.71828",
        "Olá Maria"
    ]
    
    for user_input in inputs:
        agent.process_message(user_input)
    
    # Exibir estatísticas
    stats = logger.get_stats()
    
    print(f"\n📊 Estatísticas:")
    print(f"  - Total de logs: {stats['total_logs']}")
    print(f"  - Funções executadas: {stats['total_function_calls']}")
    print(f"  - Mensagens: {stats['total_messages']}")
    print(f"  - Erros: {stats['errors']}")
    
    print(f"\n📋 Funções chamadas:")
    for func_name, count in stats["functions_called"].items():
        print(f"  - {func_name}: {count}x")
    
    # Exibir últimos 3 logs
    print(f"\n📝 Últimos 3 logs:")
    all_logs = logger.get_all_logs()
    for i, log in enumerate(all_logs[-3:], 1):
        print(f"\n  {i}. {log}")


def exemplo_6_funcoes_diretas():
    """Exemplo 6: Chamar funções diretamente"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Chamar Funções Diretamente")
    print("=" * 60)
    
    # Multiplicar
    result1 = registry.execute("multiplicar", a=7, b=8)
    print(f"\n🔧 multiplicar(7, 8) = {result1}")
    
    # Decimal
    result2 = registry.execute("calcular_decimal", valor=3.14159265359)
    print(f"🔧 calcular_decimal(3.14159265359) = {result2}")
    
    # Saudação
    result3 = registry.execute("saudacao", nome="Python")
    print(f"🔧 saudacao('Python') = {result3}")
    
    # Listar funções disponíveis
    print(f"\n📚 Funções disponíveis:")
    for func_name, description in registry.list_functions().items():
        print(f"  - {func_name}: {description}")


def exemplo_7_intent_detection():
    """Exemplo 7: Demonstrar detecção de intenção"""
    print("\n" + "=" * 60)
    print("EXEMPLO 7: Detecção de Intenção")
    print("=" * 60)
    
    agent = AIAgent()
    
    test_inputs = [
        "quanto é 5 multiplicado por 3?",
        "quero arredondar um número: 2.71828",
        "olá, meu nome é João",
        "oi, sou Pedro",
        "calcule o decimal 1.23456789",
        "quanto é 2 × 10",
        "não entendo nada"
    ]
    
    for user_input in test_inputs:
        intent = agent.detect_intent(user_input)
        print(f"\n📝 '{user_input}'")
        print(f"   → Intenção detectada: {intent if intent else '❌ Nenhuma'}")


def exemplo_8_extracao_parametros():
    """Exemplo 8: Demonstrar extração de parâmetros"""
    print("\n" + "=" * 60)
    print("EXEMPLO 8: Extração de Parâmetros")
    print("=" * 60)
    
    agent = AIAgent()
    
    test_cases = [
        ("5 multiplicado por 3", "multiplicar"),
        ("arredondar 3.14159", "calcular_decimal"),
        ("olá João Silva", "saudacao")
    ]
    
    for user_input, intent in test_cases:
        params = agent.extract_parameters(user_input, intent)
        print(f"\n📝 Input: '{user_input}'")
        print(f"   Intent: {intent}")
        print(f"   Parâmetros: {params}")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║          EXEMPLOS DE USO - AI AGENT COM FUNCTION CALLING      ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Executar exemplos
    exemplo_1_basico()
    exemplo_2_arredondamento()
    exemplo_3_saudacao()
    exemplo_4_entradas_invalidas()
    exemplo_5_logging()
    exemplo_6_funcoes_diretas()
    exemplo_7_intent_detection()
    exemplo_8_extracao_parametros()
    
    # Exibir logs finais em JSON
    print("\n" + "=" * 60)
    print("LOGS EXPORTADOS (JSON)")
    print("=" * 60)
    print(logger.export_logs_json())
