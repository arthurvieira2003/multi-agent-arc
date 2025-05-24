from typing import List, Dict, Any, Optional
import time
from datetime import datetime

from models import Task, TaskStatus, VerificationResult
from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.verification_agent import VerificationAgent

class MultiAgentSystem:
    """Sistema multi-agente que coordena o fluxo de trabalho completo"""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutionAgent()
        self.verifier = VerificationAgent()
        
        self.task_history = []
        self.system_metrics = {
            "tasks_processed": 0,
            "success_rate": 0.0,
            "average_completion_time": 0.0,
            "replanning_rate": 0.0
        }
        
        print("🚀 Sistema Multi-Agente inicializado!")
        print(f"   📋 Planner Agent: {self.planner.name}")
        print(f"   ⚙️  Execution Agent: {self.executor.name}")
        print(f"   ✅ Verification Agent: {self.verifier.name}")
        print()
    
    def process_task(self, task: Task, max_replanning_attempts: int = 2) -> Dict[str, Any]:
        """
        Processa uma tarefa através do ciclo completo:
        1. Planejamento
        2. Execução
        3. Verificação
        4. Re-planejamento (se necessário)
        """
        start_time = time.time()
        
        print(f"🎯 Iniciando processamento da tarefa: {task.title}")
        print(f"   Prioridade: {task.priority.name}")
        print(f"   Descrição: {task.description}")
        print()
        
        task.status = TaskStatus.IN_PROGRESS
        replanning_attempts = 0
        
        while replanning_attempts <= max_replanning_attempts:
            try:
                # Fase 1: Planejamento
                print("📋 FASE 1: PLANEJAMENTO")
                print("-" * 50)
                
                if replanning_attempts == 0:
                    plan = self.planner.process(task)
                else:
                    # Re-planejamento baseado nos problemas encontrados
                    issues = verification_result.issues_found if 'verification_result' in locals() else []
                    plan = self.planner.replan(task, issues)
                
                print(f"✅ Plano criado com {len(plan.subtasks)} subtarefas")
                print(f"   Tempo estimado: {plan.estimated_total_time} minutos")
                print()
                
                # Fase 2: Execução
                print("⚙️  FASE 2: EXECUÇÃO")
                print("-" * 50)
                
                execution_results = self.executor.process(plan)
                successful_executions = [r for r in execution_results if r.success]
                
                print(f"✅ Execução concluída: {len(successful_executions)}/{len(execution_results)} sucessos")
                print()
                
                # Fase 3: Verificação
                print("✅ FASE 3: VERIFICAÇÃO")
                print("-" * 50)
                
                verification_result = self.verifier.process(execution_results, task)
                
                print(f"📊 Resultado da verificação:")
                print(f"   Passou: {'✅ SIM' if verification_result.passed else '❌ NÃO'}")
                print(f"   Score de Qualidade: {verification_result.quality_score:.2f}")
                print(f"   Score de Precisão: {verification_result.accuracy_score:.2f}")
                print(f"   Problemas encontrados: {len(verification_result.issues_found)}")
                print()
                
                if verification_result.passed:
                    # Sucesso! Tarefa concluída
                    task.status = TaskStatus.COMPLETED
                    completion_time = time.time() - start_time
                    
                    result = self._create_success_result(
                        task, plan, execution_results, verification_result, 
                        completion_time, replanning_attempts
                    )
                    
                    self._update_system_metrics(completion_time, True, replanning_attempts)
                    
                    print("🎉 TAREFA CONCLUÍDA COM SUCESSO!")
                    print(f"   Tempo total: {completion_time:.1f} segundos")
                    print(f"   Tentativas de re-planejamento: {replanning_attempts}")
                    print()
                    
                    return result
                
                else:
                    # Verificação falhou - tentar re-planejamento
                    if replanning_attempts < max_replanning_attempts:
                        replanning_attempts += 1
                        task.status = TaskStatus.NEEDS_REPLANNING
                        
                        print("🔄 INICIANDO RE-PLANEJAMENTO")
                        print(f"   Tentativa {replanning_attempts}/{max_replanning_attempts}")
                        print("   Problemas identificados:")
                        for issue in verification_result.issues_found[:5]:  # Mostra apenas os primeiros 5
                            print(f"   - {issue}")
                        print()
                        
                        continue
                    else:
                        # Máximo de tentativas atingido
                        task.status = TaskStatus.FAILED
                        completion_time = time.time() - start_time
                        
                        result = self._create_failure_result(
                            task, plan, execution_results, verification_result,
                            completion_time, replanning_attempts
                        )
                        
                        self._update_system_metrics(completion_time, False, replanning_attempts)
                        
                        print("❌ TAREFA FALHOU")
                        print(f"   Máximo de tentativas de re-planejamento atingido")
                        print(f"   Tempo total: {completion_time:.1f} segundos")
                        print()
                        
                        return result
                        
            except Exception as e:
                task.status = TaskStatus.FAILED
                completion_time = time.time() - start_time
                
                error_result = {
                    "task_id": task.id,
                    "status": "failed",
                    "error": str(e),
                    "completion_time": completion_time,
                    "replanning_attempts": replanning_attempts
                }
                
                self._update_system_metrics(completion_time, False, replanning_attempts)
                
                print(f"💥 ERRO DURANTE PROCESSAMENTO: {str(e)}")
                print()
                
                return error_result
    
    def _create_success_result(self, task, plan, execution_results, verification_result, 
                             completion_time, replanning_attempts):
        """Cria resultado de sucesso detalhado"""
        return {
            "task_id": task.id,
            "status": "completed",
            "completion_time": completion_time,
            "replanning_attempts": replanning_attempts,
            "plan": {
                "id": plan.id,
                "subtasks_count": len(plan.subtasks),
                "estimated_time": plan.estimated_total_time,
                "actual_time": sum(r.execution_time for r in execution_results)
            },
            "execution": {
                "total_subtasks": len(execution_results),
                "successful_subtasks": len([r for r in execution_results if r.success]),
                "failed_subtasks": len([r for r in execution_results if not r.success]),
                "results": execution_results
            },
            "verification": {
                "passed": verification_result.passed,
                "quality_score": verification_result.quality_score,
                "accuracy_score": verification_result.accuracy_score,
                "issues_count": len(verification_result.issues_found),
                "recommendations_count": len(verification_result.recommendations)
            },
            "agents_performance": {
                "planner": self.planner.get_status()["performance_metrics"],
                "executor": self.executor.get_status()["performance_metrics"],
                "verifier": self.verifier.get_status()["performance_metrics"]
            }
        }
    
    def _create_failure_result(self, task, plan, execution_results, verification_result,
                             completion_time, replanning_attempts):
        """Cria resultado de falha detalhado"""
        return {
            "task_id": task.id,
            "status": "failed",
            "completion_time": completion_time,
            "replanning_attempts": replanning_attempts,
            "failure_reason": "verification_failed_after_max_replanning",
            "final_verification": {
                "quality_score": verification_result.quality_score,
                "accuracy_score": verification_result.accuracy_score,
                "issues_found": verification_result.issues_found,
                "recommendations": verification_result.recommendations
            },
            "execution_summary": {
                "total_subtasks": len(execution_results),
                "successful_subtasks": len([r for r in execution_results if r.success]),
                "failed_subtasks": len([r for r in execution_results if not r.success])
            }
        }
    
    def _update_system_metrics(self, completion_time: float, success: bool, replanning_attempts: int):
        """Atualiza métricas do sistema"""
        self.system_metrics["tasks_processed"] += 1
        
        # Atualiza taxa de sucesso
        total_tasks = self.system_metrics["tasks_processed"]
        current_successes = self.system_metrics["success_rate"] * (total_tasks - 1)
        if success:
            current_successes += 1
        self.system_metrics["success_rate"] = current_successes / total_tasks
        
        # Atualiza tempo médio de conclusão
        current_avg = self.system_metrics["average_completion_time"]
        self.system_metrics["average_completion_time"] = (
            (current_avg * (total_tasks - 1) + completion_time) / total_tasks
        )
        
        # Atualiza taxa de re-planejamento
        if replanning_attempts > 0:
            current_replanning = self.system_metrics["replanning_rate"] * (total_tasks - 1)
            current_replanning += 1
            self.system_metrics["replanning_rate"] = current_replanning / total_tasks
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        return {
            "system_metrics": self.system_metrics,
            "agents_status": {
                "planner": self.planner.get_status(),
                "executor": self.executor.get_status(),
                "verifier": self.verifier.get_status()
            },
            "task_history_count": len(self.task_history),
            "timestamp": datetime.now()
        }
    
    def print_system_summary(self):
        """Imprime resumo do sistema"""
        print("📊 RESUMO DO SISTEMA MULTI-AGENTE")
        print("=" * 60)
        print(f"Tarefas processadas: {self.system_metrics['tasks_processed']}")
        print(f"Taxa de sucesso: {self.system_metrics['success_rate']:.1%}")
        print(f"Tempo médio de conclusão: {self.system_metrics['average_completion_time']:.1f}s")
        print(f"Taxa de re-planejamento: {self.system_metrics['replanning_rate']:.1%}")
        print()
        
        print("🤖 PERFORMANCE DOS AGENTES")
        print("-" * 40)
        for agent_name, agent in [("Planner", self.planner), ("Executor", self.executor), ("Verifier", self.verifier)]:
            metrics = agent.performance_metrics
            print(f"{agent_name}:")
            print(f"  Tarefas: {metrics['tasks_completed']}")
            print(f"  Taxa de sucesso: {metrics['success_rate']:.1%}")
            print(f"  Tempo médio: {metrics['average_execution_time']:.1f}s")
            print()
    
    def process_multiple_tasks(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """Processa múltiplas tarefas em sequência"""
        print(f"🚀 Processando {len(tasks)} tarefas...")
        print()
        
        results = []
        for i, task in enumerate(tasks, 1):
            print(f"📋 TAREFA {i}/{len(tasks)}")
            print("=" * 60)
            
            result = self.process_task(task)
            results.append(result)
            
            print()
        
        self.print_system_summary()
        return results 