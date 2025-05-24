from typing import List, Dict, Any, Optional
import time
import random
from datetime import datetime

from .base_agent import BaseAgent
from models import Plan, SubTask, ExecutionResult, TaskStatus

class ExecutionAgent(BaseAgent):
    """Agente responsável por executar as subtarefas definidas no plano"""
    
    def __init__(self):
        super().__init__(
            name="Execution Agent",
            capabilities=[
                "task_execution",
                "code_generation",
                "file_manipulation",
                "api_integration",
                "database_operations",
                "testing_execution"
            ]
        )
        self.execution_strategies = {
            "análise": self._execute_analysis,
            "design": self._execute_design,
            "implementação": self._execute_implementation,
            "teste": self._execute_testing,
            "documentação": self._execute_documentation,
            "setup": self._execute_setup,
            "integração": self._execute_integration,
            "otimização": self._execute_optimization
        }
        self.current_executions = {}  # Track ongoing executions
    
    def process(self, plan: Plan) -> List[ExecutionResult]:
        """Executa todas as subtarefas do plano"""
        self.log_activity(f"Iniciando execução do plano {plan.id}")
        
        results = []
        executed_subtasks = set()
        
        # Executa subtarefas respeitando dependências
        while len(executed_subtasks) < len(plan.subtasks):
            ready_subtasks = self._get_ready_subtasks(plan.subtasks, executed_subtasks)
            
            if not ready_subtasks:
                # Se não há subtarefas prontas, pode haver dependência circular
                self.log_activity("Possível dependência circular detectada")
                break
            
            for subtask in ready_subtasks:
                result = self.execute_subtask(subtask)
                results.append(result)
                
                if result.success:
                    executed_subtasks.add(subtask.id)
                    subtask.status = TaskStatus.COMPLETED
                else:
                    subtask.status = TaskStatus.FAILED
                    self.log_activity(f"Falha na execução da subtarefa {subtask.title}")
        
        self.log_activity(
            f"Execução do plano concluída",
            {
                "total_subtasks": len(plan.subtasks),
                "successful": len([r for r in results if r.success]),
                "failed": len([r for r in results if not r.success])
            }
        )
        
        return results
    
    def execute_subtask(self, subtask: SubTask) -> ExecutionResult:
        """Executa uma subtarefa específica"""
        start_time = time.time()
        
        self.log_activity(f"Executando subtarefa: {subtask.title}")
        subtask.status = TaskStatus.IN_PROGRESS
        
        try:
            # Determina estratégia de execução baseada no tipo da subtarefa
            strategy = self._determine_strategy(subtask)
            
            # Executa a subtarefa
            output = self.execution_strategies[strategy](subtask)
            
            execution_time = int(time.time() - start_time)
            
            result = ExecutionResult(
                id="",
                task_id=subtask.parent_task_id,
                subtask_id=subtask.id,
                success=True,
                output=output,
                error_message=None,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            self.update_performance(execution_time, True)
            self.log_activity(f"Subtarefa {subtask.title} executada com sucesso")
            
            return result
            
        except Exception as e:
            execution_time = int(time.time() - start_time)
            
            result = ExecutionResult(
                id="",
                task_id=subtask.parent_task_id,
                subtask_id=subtask.id,
                success=False,
                output=None,
                error_message=str(e),
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            self.update_performance(execution_time, False)
            self.log_activity(f"Erro na execução da subtarefa {subtask.title}: {str(e)}")
            
            return result
    
    def _get_ready_subtasks(self, subtasks: List[SubTask], executed: set) -> List[SubTask]:
        """Retorna subtarefas que estão prontas para execução (dependências satisfeitas)"""
        ready = []
        
        for subtask in subtasks:
            if subtask.id in executed or subtask.status == TaskStatus.COMPLETED:
                continue
            
            # Verifica se todas as dependências foram executadas
            dependencies_met = all(dep_id in executed for dep_id in subtask.dependencies)
            
            if dependencies_met:
                ready.append(subtask)
        
        return ready
    
    def _determine_strategy(self, subtask: SubTask) -> str:
        """Determina a estratégia de execução baseada no título/descrição da subtarefa"""
        title_lower = subtask.title.lower()
        description_lower = subtask.description.lower()
        
        if any(keyword in title_lower for keyword in ["análise", "analisar", "requisitos"]):
            return "análise"
        elif any(keyword in title_lower for keyword in ["design", "arquitetura", "prototip"]):
            return "design"
        elif any(keyword in title_lower for keyword in ["implementa", "desenvolv", "código", "módulo"]):
            return "implementação"
        elif any(keyword in title_lower for keyword in ["teste", "validação", "verificação"]):
            return "teste"
        elif any(keyword in title_lower for keyword in ["documentação", "documentar"]):
            return "documentação"
        elif any(keyword in title_lower for keyword in ["setup", "configurar", "ambiente"]):
            return "setup"
        elif any(keyword in title_lower for keyword in ["integração", "integrar"]):
            return "integração"
        elif any(keyword in title_lower for keyword in ["otimização", "otimizar", "performance"]):
            return "otimização"
        else:
            return "implementação"  # estratégia padrão
    
    def _execute_analysis(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de análise"""
        # Simula análise de requisitos
        time.sleep(random.uniform(1, 3))  # Simula tempo de processamento
        
        analysis_result = {
            "type": "analysis",
            "requirements_identified": [
                "Requisito funcional 1: Sistema deve permitir login",
                "Requisito funcional 2: Sistema deve gerenciar dados",
                "Requisito não-funcional 1: Performance < 2s",
                "Requisito não-funcional 2: Disponibilidade 99.9%"
            ],
            "stakeholders": ["Usuários finais", "Administradores", "Desenvolvedores"],
            "constraints": ["Orçamento limitado", "Prazo de 3 meses", "Tecnologia específica"],
            "risks": ["Mudança de requisitos", "Complexidade técnica", "Recursos limitados"]
        }
        
        return analysis_result
    
    def _execute_design(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de design e arquitetura"""
        time.sleep(random.uniform(2, 4))
        
        design_result = {
            "type": "design",
            "architecture_pattern": "MVC (Model-View-Controller)",
            "components": [
                {"name": "Frontend", "technology": "React", "responsibility": "Interface do usuário"},
                {"name": "Backend", "technology": "Python/FastAPI", "responsibility": "Lógica de negócio"},
                {"name": "Database", "technology": "PostgreSQL", "responsibility": "Persistência de dados"}
            ],
            "interfaces": [
                {"name": "REST API", "endpoints": ["/users", "/tasks", "/reports"]},
                {"name": "Database Schema", "tables": ["users", "tasks", "logs"]}
            ],
            "design_patterns": ["Repository Pattern", "Factory Pattern", "Observer Pattern"]
        }
        
        return design_result
    
    def _execute_implementation(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de implementação"""
        time.sleep(random.uniform(3, 6))
        
        # Simula geração de código
        implementation_result = {
            "type": "implementation",
            "files_created": [
                "main.py",
                "models.py", 
                "controllers.py",
                "services.py",
                "utils.py"
            ],
            "lines_of_code": random.randint(200, 800),
            "functions_implemented": [
                "user_authentication()",
                "data_validation()",
                "business_logic_processor()",
                "error_handler()"
            ],
            "dependencies_added": ["fastapi", "sqlalchemy", "pydantic", "pytest"],
            "code_quality_score": random.uniform(0.7, 0.95)
        }
        
        return implementation_result
    
    def _execute_testing(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de teste"""
        time.sleep(random.uniform(2, 4))
        
        testing_result = {
            "type": "testing",
            "test_types": ["Unit Tests", "Integration Tests", "End-to-End Tests"],
            "tests_executed": random.randint(15, 50),
            "tests_passed": random.randint(12, 48),
            "coverage_percentage": random.uniform(75, 95),
            "bugs_found": random.randint(0, 5),
            "performance_metrics": {
                "response_time_avg": f"{random.uniform(0.1, 2.0):.2f}s",
                "memory_usage": f"{random.randint(50, 200)}MB",
                "cpu_usage": f"{random.randint(10, 60)}%"
            }
        }
        
        return testing_result
    
    def _execute_documentation(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de documentação"""
        time.sleep(random.uniform(1, 3))
        
        documentation_result = {
            "type": "documentation",
            "documents_created": [
                "README.md",
                "API_Documentation.md",
                "User_Manual.pdf",
                "Technical_Specification.md"
            ],
            "pages_written": random.randint(10, 50),
            "sections": [
                "Introdução",
                "Instalação",
                "Configuração", 
                "Uso",
                "API Reference",
                "Troubleshooting"
            ],
            "diagrams_created": ["Architecture Diagram", "Flow Chart", "Database Schema"]
        }
        
        return documentation_result
    
    def _execute_setup(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de configuração"""
        time.sleep(random.uniform(1, 2))
        
        setup_result = {
            "type": "setup",
            "environment_configured": True,
            "tools_installed": [
                "Python 3.9+",
                "Node.js",
                "Docker",
                "PostgreSQL",
                "Redis"
            ],
            "config_files": [
                "requirements.txt",
                "docker-compose.yml",
                ".env",
                "config.yaml"
            ],
            "environment_variables": ["DATABASE_URL", "SECRET_KEY", "DEBUG_MODE"]
        }
        
        return setup_result
    
    def _execute_integration(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de integração"""
        time.sleep(random.uniform(2, 5))
        
        integration_result = {
            "type": "integration",
            "modules_integrated": ["Frontend", "Backend", "Database", "Authentication"],
            "apis_connected": ["Payment Gateway", "Email Service", "Analytics"],
            "data_flow_verified": True,
            "integration_tests_passed": random.randint(8, 15),
            "performance_impact": f"{random.uniform(-5, 15):.1f}% change in response time"
        }
        
        return integration_result
    
    def _execute_optimization(self, subtask: SubTask) -> Dict[str, Any]:
        """Executa tarefas de otimização"""
        time.sleep(random.uniform(2, 4))
        
        optimization_result = {
            "type": "optimization",
            "optimizations_applied": [
                "Database query optimization",
                "Caching implementation",
                "Code refactoring",
                "Resource compression"
            ],
            "performance_improvements": {
                "response_time": f"{random.uniform(10, 40):.1f}% faster",
                "memory_usage": f"{random.uniform(5, 25):.1f}% reduction",
                "cpu_usage": f"{random.uniform(8, 30):.1f}% reduction"
            },
            "metrics_before": {
                "avg_response_time": f"{random.uniform(2, 5):.2f}s",
                "memory_usage": f"{random.randint(200, 400)}MB"
            },
            "metrics_after": {
                "avg_response_time": f"{random.uniform(1, 3):.2f}s", 
                "memory_usage": f"{random.randint(150, 300)}MB"
            }
        }
        
        return optimization_result 