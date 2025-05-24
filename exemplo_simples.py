#!/usr/bin/env python3
"""
Exemplo Simples do Sistema Multi-Agente
=======================================

Este é um exemplo básico de como usar o sistema multi-agente para processar uma tarefa.
"""

from datetime import datetime
from models import Task, TaskPriority, TaskStatus
from multi_agent_system import MultiAgentSystem

def main():
    print("🤖 EXEMPLO SIMPLES - SISTEMA MULTI-AGENTE")
    print("=" * 60)
    print()
    
    # Criar sistema multi-agente
    system = MultiAgentSystem()
    
    # Criar uma tarefa simples
    task = Task(
        id="",
        title="Criar Sistema de Login",
        description="Desenvolver sistema de autenticação com login e logout",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Tela de login",
            "Validação de credenciais",
            "Sistema de sessão",
            "Logout seguro"
        ],
        expected_output="Sistema de login funcional"
    )
    
    print(f"📋 Processando tarefa: {task.title}")
    print(f"   Prioridade: {task.priority.name}")
    print(f"   Requisitos: {len(task.requirements)} itens")
    print()
    
    # Processar a tarefa
    result = system.process_task(task)
    
    # Mostrar resultado
    print("📊 RESULTADO:")
    print("-" * 30)
    print(f"Status: {result['status']}")
    print(f"Tempo: {result['completion_time']:.1f}s")
    
    if result['status'] == 'completed':
        print(f"Qualidade: {result['verification']['quality_score']:.2f}")
        print(f"Precisão: {result['verification']['accuracy_score']:.2f}")
        print(f"Subtarefas: {result['plan']['subtasks_count']}")
        print(f"Re-planejamentos: {result['replanning_attempts']}")
    
    print()
    print("✅ Exemplo concluído!")

if __name__ == "__main__":
    main() 