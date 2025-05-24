from typing import List, Dict, Any
import time
from datetime import datetime

from .base_agent import BaseAgent
from models import Task, SubTask, Plan, TaskStatus, TaskPriority

class PlannerAgent(BaseAgent):
    """Agente responsável por quebrar problemas complexos em subtarefas executáveis"""
    
    def __init__(self):
        super().__init__(
            name="Planner Agent",
            capabilities=[
                "problem_breakdown",
                "task_decomposition", 
                "dependency_analysis",
                "time_estimation",
                "priority_assignment"
            ]
        )
        self.planning_strategies = {
            "sequential": self._sequential_planning,
            "parallel": self._parallel_planning,
            "hybrid": self._hybrid_planning
        }
    
    def process(self, task: Task) -> Plan:
        """Processa uma tarefa e cria um plano de execução"""
        start_time = time.time()
        
        self.log_activity(f"Iniciando planejamento para tarefa: {task.title}")
        
        try:
            # Analisa a complexidade da tarefa
            complexity = self._analyze_complexity(task)
            
            # Escolhe estratégia de planejamento baseada na complexidade
            strategy = self._choose_strategy(complexity, task.priority)
            
            # Quebra a tarefa em subtarefas
            subtasks = self._decompose_task(task, strategy)
            
            # Estima tempo total
            total_time = sum(subtask.estimated_time for subtask in subtasks)
            
            # Cria o plano
            plan = Plan(
                id="",  # será gerado automaticamente
                task_id=task.id,
                subtasks=subtasks,
                estimated_total_time=total_time,
                created_at=datetime.now(),
                agent_id=self.id
            )
            
            execution_time = time.time() - start_time
            self.update_performance(execution_time, True)
            
            self.log_activity(
                "Planejamento concluído com sucesso",
                {
                    "subtasks_created": len(subtasks),
                    "estimated_time": f"{total_time} minutos",
                    "strategy_used": strategy
                }
            )
            
            return plan
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.update_performance(execution_time, False)
            
            self.log_activity(f"Erro no planejamento: {str(e)}")
            raise
    
    def _analyze_complexity(self, task: Task) -> str:
        """Analisa a complexidade da tarefa"""
        complexity_factors = 0
        
        # Fatores que aumentam complexidade
        if len(task.requirements) > 5:
            complexity_factors += 1
        if len(task.description.split()) > 100:
            complexity_factors += 1
        if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]:
            complexity_factors += 1
        if "integração" in task.description.lower():
            complexity_factors += 1
        if "api" in task.description.lower():
            complexity_factors += 1
        
        if complexity_factors >= 3:
            return "high"
        elif complexity_factors >= 1:
            return "medium"
        else:
            return "low"
    
    def _choose_strategy(self, complexity: str, priority: TaskPriority) -> str:
        """Escolhe estratégia de planejamento baseada na complexidade e prioridade"""
        if complexity == "high" or priority == TaskPriority.CRITICAL:
            return "hybrid"
        elif complexity == "medium":
            return "parallel"
        else:
            return "sequential"
    
    def _decompose_task(self, task: Task, strategy: str) -> List[SubTask]:
        """Decompõe a tarefa em subtarefas usando a estratégia escolhida"""
        return self.planning_strategies[strategy](task)
    
    def _sequential_planning(self, task: Task) -> List[SubTask]:
        """Planejamento sequencial - uma subtarefa após a outra"""
        subtasks = []
        
        # Subtarefas básicas para qualquer tarefa
        base_subtasks = [
            ("Análise de Requisitos", "Analisar e documentar todos os requisitos", 30, []),
            ("Design da Solução", "Criar design e arquitetura da solução", 45, ["1"]),
            ("Implementação", "Implementar a solução conforme o design", 120, ["2"]),
            ("Testes", "Executar testes e validações", 60, ["3"]),
            ("Documentação", "Criar documentação final", 30, ["4"])
        ]
        
        for i, (title, description, time_est, deps) in enumerate(base_subtasks, 1):
            subtask = SubTask(
                id=str(i),
                parent_task_id=task.id,
                title=title,
                description=description,
                order=i,
                status=TaskStatus.PENDING,
                estimated_time=time_est,
                dependencies=deps
            )
            subtasks.append(subtask)
        
        return subtasks
    
    def _parallel_planning(self, task: Task) -> List[SubTask]:
        """Planejamento paralelo - algumas subtarefas podem ser executadas em paralelo"""
        subtasks = []
        
        parallel_subtasks = [
            ("Análise de Requisitos", "Analisar e documentar todos os requisitos", 30, []),
            ("Pesquisa de Tecnologias", "Pesquisar tecnologias e ferramentas", 45, []),
            ("Design da Arquitetura", "Criar arquitetura do sistema", 60, ["1"]),
            ("Setup do Ambiente", "Configurar ambiente de desenvolvimento", 30, ["2"]),
            ("Implementação Core", "Implementar funcionalidades principais", 90, ["3", "4"]),
            ("Implementação UI", "Implementar interface do usuário", 60, ["3", "4"]),
            ("Testes Unitários", "Criar e executar testes unitários", 45, ["5"]),
            ("Testes de Integração", "Executar testes de integração", 30, ["5", "6"]),
            ("Documentação", "Criar documentação completa", 40, ["7", "8"])
        ]
        
        for i, (title, description, time_est, deps) in enumerate(parallel_subtasks, 1):
            subtask = SubTask(
                id=str(i),
                parent_task_id=task.id,
                title=title,
                description=description,
                order=i,
                status=TaskStatus.PENDING,
                estimated_time=time_est,
                dependencies=deps
            )
            subtasks.append(subtask)
        
        return subtasks
    
    def _hybrid_planning(self, task: Task) -> List[SubTask]:
        """Planejamento híbrido - combina abordagens sequencial e paralela"""
        subtasks = []
        
        # Planejamento mais detalhado para tarefas complexas
        hybrid_subtasks = [
            ("Análise Detalhada", "Análise profunda de requisitos e restrições", 45, []),
            ("Prototipagem", "Criar protótipo inicial", 60, ["1"]),
            ("Validação do Protótipo", "Validar protótipo com stakeholders", 30, ["2"]),
            ("Arquitetura Detalhada", "Definir arquitetura detalhada", 75, ["3"]),
            ("Setup Avançado", "Configurar ambiente e ferramentas", 45, ["4"]),
            ("Implementação Módulo A", "Implementar primeiro módulo", 90, ["5"]),
            ("Implementação Módulo B", "Implementar segundo módulo", 90, ["5"]),
            ("Integração de Módulos", "Integrar todos os módulos", 60, ["6", "7"]),
            ("Testes Abrangentes", "Executar bateria completa de testes", 75, ["8"]),
            ("Otimização", "Otimizar performance e recursos", 45, ["9"]),
            ("Documentação Técnica", "Criar documentação técnica", 30, ["10"]),
            ("Documentação do Usuário", "Criar documentação do usuário", 30, ["10"])
        ]
        
        for i, (title, description, time_est, deps) in enumerate(hybrid_subtasks, 1):
            subtask = SubTask(
                id=str(i),
                parent_task_id=task.id,
                title=title,
                description=description,
                order=i,
                status=TaskStatus.PENDING,
                estimated_time=time_est,
                dependencies=deps
            )
            subtasks.append(subtask)
        
        return subtasks
    
    def replan(self, task: Task, issues: List[str]) -> Plan:
        """Re-planeja uma tarefa baseado em problemas encontrados"""
        self.log_activity(f"Re-planejando tarefa {task.title} devido a problemas", {"issues": issues})
        
        # Ajusta a estratégia baseada nos problemas encontrados
        if any("tempo" in issue.lower() for issue in issues):
            # Se há problemas de tempo, usa estratégia mais paralela
            strategy = "parallel"
        elif any("qualidade" in issue.lower() for issue in issues):
            # Se há problemas de qualidade, usa estratégia mais detalhada
            strategy = "hybrid"
        else:
            # Caso geral, usa estratégia sequencial mais conservadora
            strategy = "sequential"
        
        # Cria novo plano
        subtasks = self.planning_strategies[strategy](task)
        
        # Adiciona buffer de tempo baseado nos problemas
        for subtask in subtasks:
            subtask.estimated_time = int(subtask.estimated_time * 1.2)  # 20% de buffer
        
        total_time = sum(subtask.estimated_time for subtask in subtasks)
        
        return Plan(
            id="",
            task_id=task.id,
            subtasks=subtasks,
            estimated_total_time=total_time,
            created_at=datetime.now(),
            agent_id=self.id
        ) 