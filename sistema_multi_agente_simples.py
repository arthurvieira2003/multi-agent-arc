#!/usr/bin/env python3
"""
Sistema Multi-Agente Simples
============================

Implementação simplificada da arquitetura multi-agente em um único arquivo.
Baseado no diagrama: Requests → Planner → Execution → Verification → Completed Tasks
"""

import time
import random
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum

# ============================================================================
# MODELOS DE DADOS
# ============================================================================

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    title: str
    description: str
    requirements: List[str]

@dataclass
class SubTask:
    name: str
    estimated_time: int  # segundos

@dataclass
class Plan:
    subtasks: List[SubTask]
    total_time: int

@dataclass
class ExecutionResult:
    subtask_name: str
    success: bool
    output: str
    execution_time: int

@dataclass
class VerificationResult:
    passed: bool
    quality_score: float
    issues: List[str]

# ============================================================================
# AGENTES
# ============================================================================

class PlannerAgent:
    """Agente que quebra tarefas em subtarefas"""
    
    def plan(self, task: Task) -> Plan:
        print(f"📋 Planner: Analisando tarefa '{task.title}'")
        
        # Cria subtarefas baseadas nos requisitos
        subtasks = [
            SubTask("Análise de Requisitos", 5),
            SubTask("Design da Solução", 8),
            SubTask("Implementação", 15),
            SubTask("Testes", 10),
            SubTask("Documentação", 5)
        ]
        
        total_time = sum(st.estimated_time for st in subtasks)
        plan = Plan(subtasks, total_time)
        
        print(f"   ✅ Plano criado: {len(subtasks)} subtarefas, {total_time}s estimados")
        return plan

class ExecutionAgent:
    """Agente que executa as subtarefas"""
    
    def execute(self, plan: Plan) -> List[ExecutionResult]:
        print(f"⚙️  Executor: Iniciando execução de {len(plan.subtasks)} subtarefas")
        
        results = []
        for subtask in plan.subtasks:
            print(f"   🔄 Executando: {subtask.name}")
            
            # Simula execução
            start_time = time.time()
            time.sleep(random.uniform(1, 3))  # Simula trabalho
            execution_time = int(time.time() - start_time)
            
            # Simula resultado (95% de chance de sucesso)
            success = random.random() > 0.05
            output = f"Resultado da {subtask.name.lower()}" if success else "Erro na execução"
            
            result = ExecutionResult(subtask.name, success, output, execution_time)
            results.append(result)
            
            status = "✅" if success else "❌"
            print(f"   {status} {subtask.name}: {execution_time}s")
        
        successful = sum(1 for r in results if r.success)
        print(f"   📊 Execução concluída: {successful}/{len(results)} sucessos")
        return results

class VerificationAgent:
    """Agente que verifica qualidade dos resultados"""
    
    def verify(self, results: List[ExecutionResult], task: Task) -> VerificationResult:
        print(f"✅ Verificador: Analisando {len(results)} resultados")
        
        # Calcula métricas
        successful_results = [r for r in results if r.success]
        success_rate = len(successful_results) / len(results)
        
        # Calcula score de qualidade
        quality_score = success_rate * 0.9 + random.uniform(0.05, 0.1)
        quality_score = min(1.0, quality_score)
        
        # Identifica problemas
        issues = []
        if success_rate < 1.0:
            failed_tasks = [r.subtask_name for r in results if not r.success]
            issues.append(f"Falhas em: {', '.join(failed_tasks)}")
        
        if quality_score < 0.8:
            issues.append("Qualidade abaixo do esperado")
        
        # Determina se passou
        passed = success_rate >= 0.8 and quality_score >= 0.7
        
        print(f"   📊 Qualidade: {quality_score:.2f}")
        print(f"   📊 Taxa de sucesso: {success_rate:.1%}")
        print(f"   📊 Resultado: {'✅ PASSOU' if passed else '❌ FALHOU'}")
        
        if issues:
            print(f"   ⚠️  Problemas: {', '.join(issues)}")
        
        return VerificationResult(passed, quality_score, issues)

# ============================================================================
# SISTEMA MULTI-AGENTE
# ============================================================================

class MultiAgentSystem:
    """Sistema que coordena os três agentes"""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutionAgent()
        self.verifier = VerificationAgent()
    
    def process_task(self, task: Task, max_attempts: int = 2) -> Dict[str, Any]:
        print(f"🚀 Sistema Multi-Agente: Processando '{task.title}'")
        print("-" * 60)
        
        for attempt in range(max_attempts):
            if attempt > 0:
                print(f"\n🔄 Tentativa {attempt + 1}/{max_attempts} (Re-planejamento)")
                print("-" * 60)
            
            # Fase 1: Planejamento
            plan = self.planner.plan(task)
            
            # Fase 2: Execução
            execution_results = self.executor.execute(plan)
            
            # Fase 3: Verificação
            verification = self.verifier.verify(execution_results, task)
            
            if verification.passed:
                print(f"\n🎉 SUCESSO! Tarefa concluída na tentativa {attempt + 1}")
                return {
                    "status": "completed",
                    "attempts": attempt + 1,
                    "quality_score": verification.quality_score,
                    "execution_results": execution_results
                }
            else:
                print(f"\n⚠️  Verificação falhou. Problemas: {', '.join(verification.issues)}")
                if attempt < max_attempts - 1:
                    print("🔄 Iniciando re-planejamento...")
        
        print(f"\n❌ FALHA! Tarefa não concluída após {max_attempts} tentativas")
        return {
            "status": "failed",
            "attempts": max_attempts,
            "final_issues": verification.issues
        }

# ============================================================================
# DEMONSTRAÇÃO
# ============================================================================

def main():
    print("🤖 SISTEMA MULTI-AGENTE SIMPLES")
    print("=" * 60)
    print("Arquitetura: Requests → Planner → Executor → Verifier → Results")
    print("=" * 60)
    
    # Criar sistema
    system = MultiAgentSystem()
    
    # Exemplo 1: Tarefa simples
    print("\n📋 EXEMPLO 1: Desenvolvimento de API")
    task1 = Task(
        title="API de Usuários",
        description="Desenvolver API REST para gerenciar usuários",
        requirements=["CRUD", "Autenticação", "Validação", "Testes"]
    )
    
    result1 = system.process_task(task1)
    print(f"Resultado: {result1['status']} em {result1['attempts']} tentativa(s)")
    
    # Exemplo 2: Tarefa mais complexa
    print("\n📋 EXEMPLO 2: Sistema de Relatórios")
    task2 = Task(
        title="Dashboard de Relatórios",
        description="Sistema completo de relatórios com gráficos",
        requirements=["Interface Web", "Gráficos", "Exportação PDF", "Agendamento", "Cache"]
    )
    
    result2 = system.process_task(task2)
    print(f"Resultado: {result2['status']} em {result2['attempts']} tentativa(s)")
    
    print("\n🎯 DEMONSTRAÇÃO CONCLUÍDA!")
    print("O sistema demonstrou com sucesso:")
    print("✅ Planejamento automático de tarefas")
    print("✅ Execução coordenada de subtarefas")
    print("✅ Verificação de qualidade")
    print("✅ Re-planejamento quando necessário")

if __name__ == "__main__":
    main() 