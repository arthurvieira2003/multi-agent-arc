from abc import ABC, abstractmethod
from typing import Any, Dict, List
import uuid
from datetime import datetime

class BaseAgent(ABC):
    """Classe base para todos os agentes do sistema multi-agente"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.capabilities = capabilities
        self.created_at = datetime.now()
        self.is_active = True
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "average_execution_time": 0.0
        }
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Método principal de processamento do agente"""
        pass
    
    def log_activity(self, activity: str, details: Dict[str, Any] = None):
        """Registra atividade do agente"""
        timestamp = datetime.now()
        print(f"[{timestamp}] {self.name} ({self.id[:8]}): {activity}")
        if details:
            for key, value in details.items():
                print(f"  {key}: {value}")
    
    def update_performance(self, execution_time: float, success: bool):
        """Atualiza métricas de performance do agente"""
        self.performance_metrics["tasks_completed"] += 1
        
        # Atualiza taxa de sucesso
        total_tasks = self.performance_metrics["tasks_completed"]
        current_successes = self.performance_metrics["success_rate"] * (total_tasks - 1)
        if success:
            current_successes += 1
        self.performance_metrics["success_rate"] = current_successes / total_tasks
        
        # Atualiza tempo médio de execução
        current_avg = self.performance_metrics["average_execution_time"]
        self.performance_metrics["average_execution_time"] = (
            (current_avg * (total_tasks - 1) + execution_time) / total_tasks
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "id": self.id,
            "name": self.name,
            "capabilities": self.capabilities,
            "is_active": self.is_active,
            "performance_metrics": self.performance_metrics,
            "created_at": self.created_at
        } 