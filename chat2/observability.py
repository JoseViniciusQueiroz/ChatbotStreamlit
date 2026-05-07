"""
Módulo de Observabilidade com OpenTelemetry (Opcional)
Integração pronta para Jaeger, Langfuse e análise de performance
"""

import time
from functools import wraps
from typing import Any, Dict, Callable
from datetime import datetime
from logger import logger

# ============================================================================
# OBSERVABILITY SETUP (OpenTelemetry Ready)
# ============================================================================

class ObservabilityConfig:
    """Configuração de observabilidade - pode ser estendida com OTEL real"""
    
    JAEGER_ENABLED = False  # Mude para True para usar Jaeger real
    LANGFUSE_ENABLED = False  # Mude para True para usar Langfuse real
    
    JAEGER_HOST = "localhost"
    JAEGER_PORT = 6831
    
    LANGFUSE_PUBLIC_KEY = None  # Configure sua chave
    LANGFUSE_SECRET_KEY = None


class ExecutionMetrics:
    """Coleta e gerencia métricas de execução"""
    
    def __init__(self):
        self.execution_history = []
        self._initialize_otel_if_enabled()
    
    def _initialize_otel_if_enabled(self):
        """Inicializa OpenTelemetry se configurado"""
        if not ObservabilityConfig.JAEGER_ENABLED:
            return
        
        try:
            from opentelemetry import trace
            from opentelemetry.exporter.jaeger.thrift import JaegerExporter
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            
            jaeger_exporter = JaegerExporter(
                agent_host_name=ObservabilityConfig.JAEGER_HOST,
                agent_port=ObservabilityConfig.JAEGER_PORT,
            )
            
            trace.set_tracer_provider(TracerProvider())
            trace.get_tracer_provider().add_span_processor(
                BatchSpanProcessor(jaeger_exporter)
            )
            
            self.tracer = trace.get_tracer(__name__)
            self.otel_enabled = True
            
        except ImportError:
            print("⚠️ OpenTelemetry não instalado. Usando fallback.")
            self.otel_enabled = False
    
    def _initialize_langfuse_if_enabled(self):
        """Inicializa Langfuse se configurado"""
        if not ObservabilityConfig.LANGFUSE_ENABLED:
            return
        
        try:
            from langfuse import Langfuse
            
            self.langfuse = Langfuse(
                public_key=ObservabilityConfig.LANGFUSE_PUBLIC_KEY,
                secret_key=ObservabilityConfig.LANGFUSE_SECRET_KEY
            )
            self.langfuse_enabled = True
            
        except ImportError:
            print("⚠️ Langfuse não instalado. Usando fallback.")
            self.langfuse_enabled = False
    
    def track_execution(
        self,
        function_name: str,
        params: Dict[str, Any],
        result: Any,
        execution_time_ms: float,
        error: str = None
    ) -> Dict[str, Any]:
        """Registra execução com métricas detalhadas"""
        
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "function": function_name,
            "params": params,
            "result": result,
            "execution_time_ms": execution_time_ms,
            "error": error,
            "success": error is None,
            # Metadados para OTEL
            "trace_id": self._generate_trace_id(),
            "span_id": self._generate_span_id(),
        }
        
        self.execution_history.append(trace_data)
        
        # Log em OTEL se disponível
        if self.otel_enabled:
            self._record_otel_span(trace_data)
        
        # Log em Langfuse se disponível
        if self.langfuse_enabled:
            self._record_langfuse_trace(trace_data)
        
        return trace_data
    
    def _generate_trace_id(self) -> str:
        """Gera ID único para trace"""
        import uuid
        return str(uuid.uuid4())[:16]
    
    def _generate_span_id(self) -> str:
        """Gera ID único para span"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _record_otel_span(self, trace_data: Dict[str, Any]):
        """Registra span em OpenTelemetry"""
        if not self.otel_enabled:
            return
        
        try:
            with self.tracer.start_as_current_span(
                f"function.{trace_data['function']}"
            ) as span:
                span.set_attribute("function_name", trace_data["function"])
                span.set_attribute("execution_time_ms", trace_data["execution_time_ms"])
                span.set_attribute("parameters", str(trace_data["params"])[:500])
                span.set_attribute("result", str(trace_data["result"])[:500])
                span.set_attribute("success", trace_data["success"])
                
                if trace_data["error"]:
                    span.set_attribute("error", trace_data["error"])
                    span.set_attribute("status", "ERROR")
                else:
                    span.set_attribute("status", "OK")
        
        except Exception as e:
            logger.error(f"Erro ao registrar OTEL span: {e}")
    
    def _record_langfuse_trace(self, trace_data: Dict[str, Any]):
        """Registra trace em Langfuse"""
        try:
            self.langfuse.trace({
                "name": f"function.{trace_data['function']}",
                "input": trace_data["params"],
                "output": trace_data["result"],
                "metadata": {
                    "execution_time_ms": trace_data["execution_time_ms"],
                    "success": trace_data["success"],
                    "timestamp": trace_data["timestamp"]
                }
            })
        except Exception as e:
            logger.error(f"Erro ao registrar Langfuse trace: {e}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retorna resumo de métricas"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "total_errors": 0,
                "avg_execution_time_ms": 0,
                "success_rate": 0.0
            }
        
        total = len(self.execution_history)
        errors = sum(1 for e in self.execution_history if e["error"])
        times = [e["execution_time_ms"] for e in self.execution_history]
        
        return {
            "total_executions": total,
            "total_errors": errors,
            "success_rate": ((total - errors) / total * 100) if total > 0 else 0,
            "avg_execution_time_ms": sum(times) / len(times) if times else 0,
            "min_execution_time_ms": min(times) if times else 0,
            "max_execution_time_ms": max(times) if times else 0,
        }
    
    def export_traces(self, format: str = "json") -> str:
        """Exporta traces em formato especificado"""
        import json
        
        if format == "json":
            return json.dumps(self.execution_history, indent=2, default=str)
        
        elif format == "prometheus":
            # Formato Prometheus
            lines = []
            metrics = self.get_metrics_summary()
            
            lines.append("# HELP function_executions_total Total function executions")
            lines.append("# TYPE function_executions_total counter")
            lines.append(f"function_executions_total {metrics['total_executions']}")
            
            lines.append("# HELP function_errors_total Total function errors")
            lines.append("# TYPE function_errors_total counter")
            lines.append(f"function_errors_total {metrics['total_errors']}")
            
            lines.append("# HELP function_execution_time_ms Function execution time")
            lines.append("# TYPE function_execution_time_ms gauge")
            lines.append(f"function_execution_time_ms {metrics['avg_execution_time_ms']}")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Formato não suportado: {format}")


# ============================================================================
# DECORADORES PARA TRACING
# ============================================================================

def trace_execution(func: Callable) -> Callable:
    """Decorador para rastrear execução de funções"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        start_time = time.time()
        error = None
        result = None
        
        try:
            result = func(*args, **kwargs)
            return result
        
        except Exception as e:
            error = str(e)
            raise
        
        finally:
            execution_time_ms = (time.time() - start_time) * 1000
            
            # Registrar em sistema de métricas
            metrics = ExecutionMetrics()
            metrics.track_execution(
                function_name=func_name,
                params={"args": str(args)[:100], "kwargs": str(kwargs)[:100]},
                result=str(result)[:100] if result else None,
                execution_time_ms=execution_time_ms,
                error=error
            )
    
    return wrapper


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Ativar OTEL (opcional)
    # ObservabilityConfig.JAEGER_ENABLED = True
    
    metrics = ExecutionMetrics()
    
    # Simular execuções
    for i in range(5):
        metrics.track_execution(
            function_name="multiplicar",
            params={"a": i, "b": 2},
            result=i * 2,
            execution_time_ms=0.95 + i * 0.1,
            error=None
        )
    
    # Exibir métricas
    summary = metrics.get_metrics_summary()
    print("\n📊 Resumo de Métricas:")
    print(f"  Total de execuções: {summary['total_executions']}")
    print(f"  Erros: {summary['total_errors']}")
    print(f"  Taxa de sucesso: {summary['success_rate']:.1f}%")
    print(f"  Tempo médio: {summary['avg_execution_time_ms']:.2f}ms")
    
    # Exportar
    print("\n📤 Exportando (JSON):")
    print(metrics.export_traces(format="json")[:200] + "...")
    
    print("\n📤 Exportando (Prometheus):")
    print(metrics.export_traces(format="prometheus"))

"""
PARA USAR COM JAEGER REAL:

1. Instale Jaeger All-in-One:
   docker run -d --name jaeger \\
     -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \\
     -p 5775:5775/udp \\
     -p 6831:6831/udp \\
     -p 16686:16686 \\
     jaegertracing/all-in-one:latest

2. Configure em observability.py:
   ObservabilityConfig.JAEGER_ENABLED = True

3. Acesse Jaeger UI: http://localhost:16686

PARA USAR COM LANGFUSE:

1. Configure keys em observability.py:
   ObservabilityConfig.LANGFUSE_ENABLED = True
   ObservabilityConfig.LANGFUSE_PUBLIC_KEY = "seu-public-key"
   ObservabilityConfig.LANGFUSE_SECRET_KEY = "seu-secret-key"

2. Traces aparecerão em: https://cloud.langfuse.com/
"""
