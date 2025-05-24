#!/usr/bin/env python3
"""
Demonstração do Sistema Multi-Agente
====================================

Este exemplo mostra como usar o sistema multi-agente para processar diferentes tipos de tarefas,
demonstrando o fluxo completo de planejamento, execução e verificação.
"""

from datetime import datetime
from models import Task, TaskPriority, TaskStatus
from multi_agent_system import MultiAgentSystem

def create_sample_tasks():
    """Cria tarefas de exemplo para demonstração"""
    
    tasks = []
    
    # Tarefa 1: Desenvolvimento de API simples
    task1 = Task(
        id="",
        title="Desenvolver API REST para Gerenciamento de Usuários",
        description="Criar uma API REST completa para gerenciar usuários com operações CRUD, autenticação e documentação",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Endpoints para CRUD de usuários",
            "Sistema de autenticação JWT",
            "Validação de dados",
            "Documentação da API",
            "Testes unitários e de integração"
        ],
        expected_output="API funcional com documentação completa"
    )
    tasks.append(task1)
    
    # Tarefa 2: Sistema de relatórios
    task2 = Task(
        id="",
        title="Implementar Sistema de Relatórios",
        description="Desenvolver sistema para gerar relatórios automáticos com gráficos e exportação em PDF",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Geração de gráficos dinâmicos",
            "Exportação para PDF",
            "Interface web responsiva",
            "Agendamento de relatórios",
            "Cache de dados"
        ],
        expected_output="Sistema de relatórios funcional com interface web"
    )
    tasks.append(task2)
    
    # Tarefa 3: Integração com API externa (tarefa complexa)
    task3 = Task(
        id="",
        title="Integração com API de Pagamentos",
        description="Integrar sistema com API externa de pagamentos, incluindo webhook para notificações e tratamento de erros robusto",
        priority=TaskPriority.CRITICAL,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Integração com API de pagamentos",
            "Processamento de webhooks",
            "Tratamento de erros e retry logic",
            "Logs detalhados de transações",
            "Testes com sandbox",
            "Monitoramento de saúde da integração",
            "Documentação técnica detalhada"
        ],
        expected_output="Integração completa e robusta com API de pagamentos"
    )
    tasks.append(task3)
    
    return tasks

def demonstrate_single_task():
    """Demonstra o processamento de uma única tarefa"""
    print("🎯 DEMONSTRAÇÃO: PROCESSAMENTO DE TAREFA ÚNICA")
    print("=" * 80)
    print()
    
    # Cria sistema multi-agente
    system = MultiAgentSystem()
    
    # Cria uma tarefa de exemplo
    task = Task(
        id="",
        title="Criar Dashboard de Monitoramento",
        description="Desenvolver dashboard web para monitoramento de sistema com métricas em tempo real",
        priority=TaskPriority.HIGH,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Interface web responsiva",
            "Gráficos em tempo real",
            "Alertas configuráveis",
            "Histórico de métricas"
        ],
        expected_output="Dashboard funcional com monitoramento em tempo real"
    )
    
    # Processa a tarefa
    result = system.process_task(task)
    
    # Mostra resultado
    print("📋 RESULTADO FINAL:")
    print("-" * 40)
    print(f"Status: {result['status']}")
    print(f"Tempo de conclusão: {result['completion_time']:.1f}s")
    if result['status'] == 'completed':
        print(f"Qualidade: {result['verification']['quality_score']:.2f}")
        print(f"Precisão: {result['verification']['accuracy_score']:.2f}")
    print()

def demonstrate_multiple_tasks():
    """Demonstra o processamento de múltiplas tarefas"""
    print("🚀 DEMONSTRAÇÃO: PROCESSAMENTO DE MÚLTIPLAS TAREFAS")
    print("=" * 80)
    print()
    
    # Cria sistema multi-agente
    system = MultiAgentSystem()
    
    # Cria tarefas de exemplo
    tasks = create_sample_tasks()
    
    # Processa todas as tarefas
    results = system.process_multiple_tasks(tasks)
    
    # Análise dos resultados
    print("📊 ANÁLISE DOS RESULTADOS")
    print("=" * 60)
    
    successful_tasks = [r for r in results if r['status'] == 'completed']
    failed_tasks = [r for r in results if r['status'] == 'failed']
    
    print(f"✅ Tarefas concluídas com sucesso: {len(successful_tasks)}")
    print(f"❌ Tarefas que falharam: {len(failed_tasks)}")
    print(f"📈 Taxa de sucesso: {len(successful_tasks)/len(results):.1%}")
    print()
    
    if successful_tasks:
        avg_quality = sum(r['verification']['quality_score'] for r in successful_tasks) / len(successful_tasks)
        avg_accuracy = sum(r['verification']['accuracy_score'] for r in successful_tasks) / len(successful_tasks)
        avg_time = sum(r['completion_time'] for r in successful_tasks) / len(successful_tasks)
        
        print("📊 MÉTRICAS DAS TAREFAS CONCLUÍDAS:")
        print(f"   Qualidade média: {avg_quality:.2f}")
        print(f"   Precisão média: {avg_accuracy:.2f}")
        print(f"   Tempo médio: {avg_time:.1f}s")
        print()
    
    return results

def demonstrate_replanning():
    """Demonstra o processo de re-planejamento"""
    print("🔄 DEMONSTRAÇÃO: PROCESSO DE RE-PLANEJAMENTO")
    print("=" * 80)
    print()
    
    # Cria sistema multi-agente
    system = MultiAgentSystem()
    
    # Cria uma tarefa complexa que pode precisar de re-planejamento
    complex_task = Task(
        id="",
        title="Sistema de Machine Learning Completo",
        description="Desenvolver sistema completo de machine learning com pipeline de dados, treinamento de modelos, API de predição e monitoramento de performance",
        priority=TaskPriority.CRITICAL,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        requirements=[
            "Pipeline de processamento de dados",
            "Treinamento automatizado de modelos",
            "API REST para predições",
            "Monitoramento de drift de dados",
            "Interface web para visualização",
            "Testes automatizados",
            "Documentação técnica completa",
            "Deploy automatizado",
            "Logs e métricas detalhadas"
        ],
        expected_output="Sistema ML completo em produção"
    )
    
    # Processa com mais tentativas de re-planejamento
    result = system.process_task(complex_task, max_replanning_attempts=3)
    
    print("📋 RESULTADO DO RE-PLANEJAMENTO:")
    print("-" * 50)
    print(f"Status: {result['status']}")
    print(f"Tentativas de re-planejamento: {result['replanning_attempts']}")
    print(f"Tempo total: {result['completion_time']:.1f}s")
    print()

def main():
    """Função principal da demonstração"""
    print("🤖 SISTEMA MULTI-AGENTE - DEMONSTRAÇÃO COMPLETA")
    print("=" * 80)
    print()
    print("Este exemplo demonstra uma arquitetura multi-agente baseada na imagem fornecida,")
    print("com três agentes especializados trabalhando em conjunto:")
    print()
    print("📋 Planner Agent: Quebra problemas complexos em subtarefas")
    print("⚙️  Execution Agent: Executa as subtarefas do plano")
    print("✅ Verification Agent: Verifica qualidade e precisão dos resultados")
    print()
    print("O sistema implementa o ciclo completo mostrado na imagem:")
    print("Requests → Planning → Execution → Verification → Completed Tasks")
    print("Com re-planejamento automático quando necessário.")
    print()
    input("Pressione Enter para continuar...")
    print()
    
    # Demonstração 1: Tarefa única
    demonstrate_single_task()
    input("Pressione Enter para continuar para a próxima demonstração...")
    print()
    
    # Demonstração 2: Múltiplas tarefas
    demonstrate_multiple_tasks()
    input("Pressione Enter para continuar para a próxima demonstração...")
    print()
    
    # Demonstração 3: Re-planejamento
    demonstrate_replanning()
    
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print()
    print("O sistema multi-agente demonstrou com sucesso:")
    print("✅ Planejamento inteligente de tarefas")
    print("✅ Execução coordenada de subtarefas")
    print("✅ Verificação de qualidade automática")
    print("✅ Re-planejamento adaptativo")
    print("✅ Métricas de performance detalhadas")
    print()

if __name__ == "__main__":
    main() 