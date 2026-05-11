"""
Módulo de Observabilidade com OpenTelemetry (Opcional)
Integração pronta para Jaeger, Langfuse e análise de performance
"""

import time
from functools import wraps
from typing import Any, Dict, Callable
from datetime import datetime
from logger import logger


class ObservabilityConfig:
    """Configuração de observabilidade - pode ser estendida com OTEL real"""
    
    JAEGER_ENABLED = False
    LANGFUSE_ENABLED = False
    JAEGER_HOST = "localhost"
    JAEGER_PORT = 6831
    LANGFUSE_PUBLIC_KEY = None
    LANGFUSE_SECRET_KEY = None


class ExecutionMetrics:
    """Coleta e gerencia métricas de execução"""
    
    def __init__(self):
        self.execution_history = []
        self._initialize_otel_if_enabled()

    def _initialize_otel_if_enabled(self):
        if not ObservabilityConfig.JAEGER_ENABLED:
            self.otel_enabled = False
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
        except Exception:
            self.otel_enabled = False

    def _initialize_langfuse_if_enabled(self):
        if not ObservabilityConfig.LANGFUSE_ENABLED:
            self.langfuse_enabled = False
            return
        try:
            from langfuse import Langfuse
            self.langfuse = Langfuse(
                public_key=ObservabilityConfig.LANGFUSE_PUBLIC_KEY,
                secret_key=ObservabilityConfig.LANGFUSE_SECRET_KEY
            )
            self.langfuse_enabled = True
        except Exception:
            self.langfuse_enabled = False

    def track_execution(
        self,
        function_name: str,
        params: Dict[str, Any],
        result: Any,
        execution_time_ms: float,
        error: str = None
    ) -> Dict[str, Any]:
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "function": function_name,
            "params": params,
            "result": result,
            "execution_time_ms": execution_time_ms,
            "error": error,
            "success": error is None,
            "trace_id": self._generate_trace_id(),
            "span_id": self._generate_span_id(),
        }
        
        self.execution_history.append(trace_data)
        
        if getattr(self, "otel_enabled", False):
            self._record_otel_span(trace_data)
        if getattr(self, "langfuse_enabled", False):
            self._record_langfuse_trace(trace_data)
        
        return trace_data

    def _generate_trace_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:16]

    def _generate_span_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]

    def _record_otel_span(self, trace_data: Dict[str, Any]):
        if not getattr(self, "otel_enabled", False):
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
            logger.log_message("system", f"Erro ao registrar OTEL span: {e}")

    def _record_langfuse_trace(self, trace_data: Dict[str, Any]):
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
            logger.log_message("system", f"Erro ao registrar Langfuse trace: {e}")

    def get_metrics_summary(self) -> Dict[str, Any]:
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
        import json
        if format == "json":
            return json.dumps(self.execution_history, indent=2, default=str)
        elif format == "prometheus":
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


def trace_execution(func: Callable) -> Callable:
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
            metrics = ExecutionMetrics()
            metrics.track_execution(
                function_name=func_name,
                params={"args": str(args)[:100], "kwargs": str(kwargs)[:100]},
                result=str(result)[:100] if result else None,
                execution_time_ms=execution_time_ms,
                error=error
            )
    return wrapper
