#!/usr/bin/env python3
"""
Demonstração Visual do Sistema Multi-Agente
==========================================

Interface web interativa para demonstrar o funcionamento da arquitetura multi-agente
com visualizações em tempo real, gráficos e animações.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
import json
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any
import asyncio

# Configuração da página
st.set_page_config(
    page_title="Sistema Multi-Agente - Demo Visual",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: bold;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
    }
    
    .agent-card-active {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
        50% { box-shadow: 0 12px 24px rgba(255,107,107,0.4); }
        100% { box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .status-processing {
        color: #ffc107;
        font-weight: bold;
        font-size: 1.1rem;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.5; }
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .flow-arrow {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin: 1rem 0;
        animation: flow 2s ease-in-out infinite;
    }
    
    @keyframes flow {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
    }
    
    .task-progress {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3498db;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        border: 2px solid #3498db;
    }
    
    .task-progress h4 {
        color: #3498db;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .task-progress p {
        color: #ecf0f1;
        margin: 0.5rem 0;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .task-progress strong {
        color: #f39c12;
    }
    
    .concept-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .execution-log {
        background: #1e1e1e;
        color: #f8f8f2;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        border-left: 4px solid #50fa7b;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .log-entry {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #6272a4;
        background: #282a36;
    }
    
    .log-success {
        border-left-color: #50fa7b;
        background: #1a2e1a;
    }
    
    .log-error {
        border-left-color: #ff5555;
        background: #2e1a1a;
    }
    
    .log-warning {
        border-left-color: #f1fa8c;
        background: #2e2e1a;
    }
    
    .log-info {
        border-left-color: #8be9fd;
        background: #1a1e2e;
    }
    
    .log-timestamp {
        color: #6272a4;
        font-size: 0.8rem;
    }
    
    .log-agent {
        color: #bd93f9;
        font-weight: bold;
    }
    
    .log-task {
        color: #ffb86c;
        font-weight: bold;
    }
    
    .log-details {
        color: #f8f8f2;
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class VisualMultiAgentDemo:
    def __init__(self):
        self.agents_data = {
            "Planner Agent": {
                "icon": "🎯",
                "color": "#28a745",
                "description": "Analisa e decompõe tarefas complexas",
                "tasks_completed": 0,
                "current_status": "Idle",
                "performance": [],
                "details": [
                    "Análise de complexidade",
                    "Decomposição em subtarefas", 
                    "Mapeamento de dependências",
                    "Criação de plano de execução"
                ]
            },
            "Execution Agent": {
                "icon": "⚙️",
                "color": "#1f77b4", 
                "description": "Executa as subtarefas do plano",
                "tasks_completed": 0,
                "current_status": "Idle",
                "performance": [],
                "details": [
                    "Configuração do ambiente",
                    "Implementação de módulos",
                    "Integração de componentes",
                    "Execução de testes"
                ]
            },
            "Verification Agent": {
                "icon": "✅",
                "color": "#dc3545",
                "description": "Verifica qualidade e precisão dos resultados",
                "tasks_completed": 0,
                "current_status": "Idle",
                "performance": [],
                "details": [
                    "Análise de qualidade",
                    "Verificação de precisão",
                    "Validação de resultados",
                    "Geração de relatórios"
                ]
            }
        }
        
        self.system_metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "replanning_events": 0,
            "avg_completion_time": 0,
            "success_rate": 0,
            "current_task": None,
            "processing_step": 0
        }
        
        self.task_history = []
        self.current_task = None
        self.execution_logs = []  # Logs detalhados de execução
        
    def add_log_entry(self, level: str, agent: str, task: str, message: str, details: str = None):
        """Adiciona uma entrada no log de execução"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,  # success, error, warning, info
            "agent": agent,
            "task": task,
            "message": message,
            "details": details
        }
        self.execution_logs.append(log_entry)
    
    def display_execution_logs(self):
        """Exibe os logs de execução de forma organizada"""
        if not self.execution_logs:
            st.info("Sem logs de execução")
            return
        
        st.markdown("## Logs Detalhados de Execução")
        
        # Filtros para os logs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_levels = st.multiselect(
                "Filtrar por nível:",
                ["success", "error", "warning", "info"],
                default=["success", "error", "warning", "info"],
                key="log_levels_filter"
            )
        
        with col2:
            agents = list(self.agents_data.keys()) + ["Sistema"]
            show_agents = st.multiselect(
                "Filtrar por agente:",
                agents,
                default=agents,
                key="log_agents_filter"
            )
        
        with col3:
            if st.button("🗑️ Limpar Logs"):
                self.execution_logs = []
                st.rerun()
        
        # Exibir logs filtrados
        filtered_logs = [
            log for log in self.execution_logs 
            if log["level"] in show_levels and log["agent"] in show_agents
        ]
        
        if filtered_logs:
            # Exibir logs usando componentes nativos do Streamlit
            st.markdown("### 📜 Histórico de Execução")
            
            # Reverter ordem para mostrar mais recentes primeiro
            for i, log in enumerate(reversed(filtered_logs[-50:]), 1):
                level_icon = {
                    "success": "✅",
                    "error": "❌", 
                    "warning": "⚠️",
                    "info": "ℹ️"
                }.get(log["level"], "📝")
                
                # Determinar cor baseada no nível
                if log["level"] == "success":
                    details_text = f"🔍 {log['details']}" if log['details'] else ""
                    st.success(f"{level_icon} **[{log['timestamp']}] {log['agent']} → {log['task']}**\n\n"
                              f"📄 {log['message']}\n\n"
                              f"{details_text}")
                elif log["level"] == "error":
                    details_text = f"🔍 {log['details']}" if log['details'] else ""
                    st.error(f"{level_icon} **[{log['timestamp']}] {log['agent']} → {log['task']}**\n\n"
                            f"📄 {log['message']}\n\n"
                            f"{details_text}")
                elif log["level"] == "warning":
                    details_text = f"🔍 {log['details']}" if log['details'] else ""
                    st.warning(f"{level_icon} **[{log['timestamp']}] {log['agent']} → {log['task']}**\n\n"
                              f"📄 {log['message']}\n\n"
                              f"{details_text}")
                else:  # info
                    details_text = f"🔍 {log['details']}" if log['details'] else ""
                    st.info(f"{level_icon} **[{log['timestamp']}] {log['agent']} → {log['task']}**\n\n"
                           f"📄 {log['message']}\n\n"
                           f"{details_text}")
            
            # Estatísticas dos logs
            st.markdown("---")
            st.markdown("### Estatísticas dos Logs")
            col1, col2, col3, col4 = st.columns(4)
            
            success_count = len([l for l in filtered_logs if l["level"] == "success"])
            error_count = len([l for l in filtered_logs if l["level"] == "error"])
            warning_count = len([l for l in filtered_logs if l["level"] == "warning"])
            info_count = len([l for l in filtered_logs if l["level"] == "info"])
            
            with col1:
                st.metric("✅ Sucessos", success_count)
            with col2:
                st.metric("❌ Erros", error_count)
            with col3:
                st.metric("⚠️ Avisos", warning_count)
            with col4:
                st.metric("ℹ️ Informações", info_count)
        else:
            st.warning("Nenhum log encontrado com os filtros selecionados")
    
    def generate_detailed_execution_steps(self, agent: str, task_name: str, step: int, total_steps: int):
        """Gera etapas detalhadas de execução com retornos realistas"""
        
        execution_scenarios = {
            "Planner Agent": {
                "steps": [
                    {
                        "action": "Análise inicial da tarefa",
                        "result": f"Tarefa '{task_name}' classificada como complexidade ALTA",
                        "details": "Identificados 6 módulos principais: Autenticação, CRUD Operations, Middleware, Database Layer, API Documentation, Testing Suite"
                    },
                    {
                        "action": "Decomposição em subtarefas",
                        "result": "8 subtarefas criadas com dependências mapeadas",
                        "details": "Subtarefas: 1) Setup do projeto, 2) Configuração do banco, 3) Autenticação JWT, 4) Endpoints CRUD, 5) Middleware de validação, 6) Documentação Swagger, 7) Testes automatizados, 8) Deploy e monitoramento"
                    },
                    {
                        "action": "Estimativa de recursos e tempo",
                        "result": "Tempo estimado: 45-60 minutos para implementação completa",
                        "details": "Recursos necessários: Node.js/Express, PostgreSQL, JWT library, Swagger, Jest para testes. Estimativa baseada em complexidade dos endpoints e requisitos de segurança"
                    },
                    {
                        "action": "Criação do plano de execução",
                        "result": "Plano sequencial com 3 pontos de verificação definidos",
                        "details": "Checkpoint 1: Após autenticação (25%), Checkpoint 2: Após CRUD completo (70%), Checkpoint 3: Após testes (95%). Estratégia: desenvolvimento incremental com validação contínua"
                    },
                    {
                        "action": "Análise de riscos e contingências",
                        "result": "3 riscos principais identificados com planos de mitigação",
                        "details": "Risco 1: Falha na conexão DB (solução: pool de conexões), Risco 2: Problemas de autenticação (solução: fallback para auth básico), Risco 3: Performance inadequada (solução: cache Redis)"
                    }
                ]
            },
            "Execution Agent": {
                "steps": [
                    {
                        "action": "Configuração do ambiente de desenvolvimento",
                        "result": "Ambiente configurado com sucesso - Stack completa operacional",
                        "details": "✅ Node.js 18.x instalado, ✅ PostgreSQL 14 conectado (porta 5432), ✅ Dependências npm instaladas (express, jsonwebtoken, bcrypt, sequelize), ✅ Estrutura de pastas criada"
                    },
                    {
                        "action": "Implementação do sistema de autenticação",
                        "result": "Autenticação JWT implementada com segurança robusta",
                        "details": "📋 Endpoints: POST /auth/login, POST /auth/register, POST /auth/refresh. 🔐 Hash bcrypt (salt rounds: 12), JWT com expiração 1h, Refresh tokens com 7 dias. ✅ Middleware de validação ativo"
                    },
                    {
                        "action": "Desenvolvimento dos endpoints CRUD",
                        "result": "API REST completa com 12 endpoints implementados",
                        "details": "📍 Usuários: GET, POST, PUT, DELETE /users. 📍 Perfis: GET, POST, PUT /profiles. 📍 Configurações: GET, PUT /settings. 🛡️ Validação de entrada com Joi, sanitização de dados, rate limiting (100 req/min)"
                    },
                    {
                        "action": "Integração com APIs externas",
                        "result": "2 de 3 APIs integradas com sucesso",
                        "details": "✅ API de geolocalização (ViaCEP) - 200ms resposta média. ✅ API de notificações (SendGrid) - 150ms resposta média. ⏳ API de pagamentos (Stripe) - em integração, aguardando credenciais de produção"
                    },
                    {
                        "action": "Implementação de testes automatizados",
                        "result": "Suite de testes criada com 87% de cobertura",
                        "details": "🧪 23 testes unitários implementados, 8 testes de integração, 3 testes end-to-end. ✅ 20 testes passando, ⚠️ 3 testes com timeout (>5s), Cobertura: Controllers 95%, Models 85%, Utils 75%"
                    },
                    {
                        "action": "Otimização de performance",
                        "result": "Performance otimizada - tempo de resposta reduzido em 40%",
                        "details": "🚀 Cache Redis implementado (TTL 300s), Queries otimizadas com índices, 🔄 Connection pooling (max 20 conexões), Tempo médio: 120ms (antes: 200ms), Throughput: 500 req/s"
                    },
                    {
                        "action": "Documentação e deploy",
                        "result": "API documentada e deployada com monitoramento ativo",
                        "details": "📚 Swagger UI disponível em /api-docs, 🚀 Deploy no Heroku realizado, Monitoring com New Relic ativo, 🔍 Logs estruturados com Winston, Health check endpoint /health funcionando"
                    }
                ]
            },
            "Verification Agent": {
                "steps": [
                    {
                        "action": "Análise de qualidade do código",
                        "result": "Score de qualidade: 8.7/10 - Código em excelente estado",
                        "details": "ESLint: 2 warnings menores, Prettier: formatação OK, 🔍 Complexidade ciclomática: Baixa (média 3.2), 📝 Documentação JSDoc: 85% das funções, Arquitetura: Padrão MVC respeitado"
                    },
                    {
                        "action": "Verificação de segurança",
                        "result": "Auditoria de segurança aprovada com 1 recomendação menor",
                        "details": "🔐 Vulnerabilidades: 0 críticas, 0 altas, 1 média (rate limiting mais restritivo recomendado). ✅ SQL injection protegido, ✅ XSS protegido, ✅ CORS configurado, ⚠️ Recomendação: implementar CSRF tokens"
                    },
                    {
                        "action": "Teste de performance e carga",
                        "result": "Performance aprovada - sistema suporta carga esperada",
                        "details": "🎯 Tempo de resposta médio: 118ms (meta: <200ms), Throughput: 485 req/s (meta: >400 req/s), 💾 Uso de memória: 145MB (limite: 512MB), 🔄 Teste de carga: 1000 usuários simultâneos OK"
                    },
                    {
                        "action": "Validação de requisitos funcionais",
                        "result": "97% dos requisitos atendidos - 1 item não-crítico pendente",
                        "details": "✅ Autenticação JWT: Implementado, ✅ CRUD completo: Implementado, ✅ Validação de dados: Implementado, ✅ Documentação API: Implementado, ⏳ Relatórios em PDF: Pendente (não-crítico)"
                    },
                    {
                        "action": "Verificação de conformidade e padrões",
                        "result": "API em conformidade com padrões REST e OpenAPI 3.0",
                        "details": "📋 REST principles: Respeitados, HTTP status codes: Corretos, 🔗 HATEOAS: Implementado parcialmente, 📝 OpenAPI 3.0: Spec válida, 🌐 Content-Type: application/json consistente"
                    },
                    {
                        "action": "Relatório final de qualidade",
                        "result": "Sistema aprovado para produção com score final 9.1/10",
                        "details": "🎉 Qualidade geral: Excelente, 🔒 Segurança: Muito boa, ⚡ Performance: Ótima, 📚 Documentação: Boa, 🧪 Testes: Muito bom. Recomendação: Deploy autorizado com monitoramento contínuo"
                    }
                ]
            }
        }
        
        agent_scenarios = execution_scenarios.get(agent, {"steps": []})
        if step < len(agent_scenarios["steps"]):
            return agent_scenarios["steps"][step]
        else:
            return {
                "action": f"Finalizando processamento - Etapa {step + 1}",
                "result": "Processamento concluído com sucesso",
                "details": f"Todas as verificações finais realizadas. Agente {agent} finalizou sua contribuição para a tarefa '{task_name}' com status: APROVADO"
            }
    
    def generate_error_scenarios(self, agent: str, task_name: str):
        """Gera cenários de erro realistas"""
        
        error_scenarios = {
            "Planner Agent": [
                {
                    "error": "Dependência circular detectada na decomposição",
                    "details": "Subtarefa 'Autenticação' depende de 'Middleware', que depende de 'Database', que depende de 'Autenticação'. Ciclo infinito identificado no grafo de dependências",
                    "solution": "Reestruturação do plano: Separação da autenticação em 2 fases (básica + avançada), implementação do middleware genérico primeiro, depois especialização para autenticação"
                },
                {
                    "error": "Recursos insuficientes para complexidade estimada",
                    "details": "Tarefa requer 8GB RAM e 4 cores CPU, mas ambiente disponível tem apenas 4GB RAM e 2 cores. Estimativa de tempo aumentaria de 45min para 2h30min",
                    "solution": "Divisão da tarefa em 3 subtarefas menores executadas sequencialmente, implementação de cache para reduzir uso de memória, otimização de queries para reduzir processamento"
                },
                {
                    "error": "Conflito de prioridades entre requisitos",
                    "details": "Requisito de 'alta performance' (tempo resposta <100ms) conflita com 'máxima segurança' (múltiplas validações). Trade-off identificado entre velocidade e segurança",
                    "solution": "Implementação de estratégia híbrida: cache para endpoints públicos (performance), validação completa para endpoints críticos (segurança), configuração por perfil de usuário"
                }
            ],
            "Execution Agent": [
                {
                    "error": "Falha na conexão com API externa crítica",
                    "details": "API de pagamentos (Stripe) retornou erro 503 - Service Unavailable. Timeout após 30s. Endpoint /v1/charges inacessível. Impacto: 40% da funcionalidade comprometida",
                    "solution": "Implementação de circuit breaker pattern, fallback para gateway de pagamento secundário (PayPal), queue de retry com backoff exponencial (1s, 2s, 4s, 8s), notificação para admin"
                },
                {
                    "error": "Timeout na execução de testes de integração",
                    "details": "Teste 'POST /users/bulk-import' excedeu limite de 30 segundos. Processamento de 10.000 registros causou deadlock no banco. Memory leak detectado no processo",
                    "solution": "Implementação de processamento em lotes (batch de 100 registros), otimização de queries com índices compostos, aumento do timeout para 60s, implementação de cleanup de memória"
                },
                {
                    "error": "Conflito de dependências no ambiente",
                    "details": "Biblioteca 'jsonwebtoken' versão 9.0 incompatível com 'express-jwt' versão 6.1. Conflito de tipos TypeScript. Build falhando com 23 erros de compilação",
                    "solution": "Downgrade controlado: jsonwebtoken@8.5.1, atualização express-jwt@7.7.5, ajuste dos tipos @types/jsonwebtoken@8.5.8, teste de regressão completo"
                },
                {
                    "error": "Falha na migração do banco de dados",
                    "details": "Migration 'add_user_preferences_table' falhou. Constraint violation: foreign key 'user_id' referencia tabela inexistente. Rollback automático executado",
                    "solution": "Correção da ordem das migrations, criação da tabela 'users' antes de 'user_preferences', implementação de verificação de dependências, backup automático antes de migrations"
                }
            ],
            "Verification Agent": [
                {
                    "error": "Falha crítica nos testes de segurança",
                    "details": "Vulnerabilidade de SQL Injection detectada no endpoint POST /users/search. Parâmetro 'query' não sanitizado permite execução de comandos SQL arbitrários. CVSS Score: 9.8 (Crítico)",
                    "solution": "Implementação imediata de prepared statements, sanitização com biblioteca 'validator.js', implementação de WAF (Web Application Firewall), auditoria completa de todos os endpoints"
                },
                {
                    "error": "Performance abaixo do aceitável em teste de carga",
                    "details": "Tempo de resposta médio: 850ms (meta: <200ms). Throughput: 45 req/s (meta: >400 req/s). Gargalo identificado: queries N+1 no endpoint /users com relacionamentos",
                    "solution": "Implementação de eager loading com Sequelize, cache Redis com TTL 300s, otimização de queries com EXPLAIN ANALYZE, implementação de CDN para assets estáticos"
                },
                {
                    "error": "Cobertura de testes insuficiente para produção",
                    "details": "Cobertura atual: 65% (mínimo exigido: 80%). Módulos críticos sem testes: AuthController (45%), PaymentService (30%), UserValidator (55%). 12 funções sem cobertura",
                    "solution": "Criação de 18 testes adicionais para módulos críticos, implementação de testes de contrato para APIs externas, configuração de quality gate no CI/CD, bloqueio de deploy se <80%"
                },
                {
                    "error": "Violação de padrões de arquitetura",
                    "details": "Acoplamento alto detectado: Controller acessando diretamente o banco (violação MVC). Responsabilidade única violada em UserService (autenticação + CRUD + validação)",
                    "solution": "Refatoração para padrão Repository, separação em AuthService + UserService + ValidationService, implementação de interfaces para desacoplamento, aplicação de SOLID principles"
                },
                {
                    "error": "Documentação da API inconsistente",
                    "details": "Swagger spec diverge da implementação real. 8 endpoints não documentados, 5 schemas com tipos incorretos, exemplos de request/response desatualizados",
                    "solution": "Sincronização automática Swagger com decorators, implementação de testes de contrato OpenAPI, validação automática no CI/CD, geração de docs a partir do código"
                }
            ]
        }
        
        agent_errors = error_scenarios.get(agent, [])
        if agent_errors:
            return random.choice(agent_errors)
        else:
            return {
                "error": "Erro inesperado no processamento",
                "details": f"Falha não catalogada durante execução do {agent}. Stack trace capturado, logs enviados para análise. Impacto: processamento interrompido temporariamente",
                "solution": f"Reinicialização do {agent} com parâmetros de fallback, ativação de modo de recuperação automática, escalação para equipe de suporte técnico"
            }
    
    def create_architecture_diagram(self):
        """Cria diagrama da arquitetura multi-agente com animações"""
        fig = go.Figure()
        
        # Posições dos componentes
        positions = {
            "📥 Entrada": (0, 2),
            "🎯 Planner": (2, 3),
            "⚙️ Execution": (4, 2),
            "✅ Verification": (4, 0),
            "📤 Saída": (6, 2)
        }
        
        # Cores baseadas no status atual
        colors = {}
        for name, (x, y) in positions.items():
            if "Entrada" in name or "Saída" in name:
                colors[name] = "#28a745"
            elif self.current_task:
                # Destacar agente ativo
                agent_name = name.split(" ")[1] if len(name.split(" ")) > 1 else name
                if agent_name in self.current_task.get("current_agent", ""):
                    colors[name] = "#ff6b6b"  # Vermelho para ativo
                else:
                    colors[name] = "#1f77b4"
            else:
                colors[name] = "#1f77b4"
        
        # Adicionar nós
        for name, (x, y) in positions.items():
            size = 100 if name in colors and colors[name] == "#ff6b6b" else 80
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(size=size, color=colors[name], line=dict(width=3, color="white")),
                text=name,
                textposition="middle center",
                textfont=dict(color="white", size=10, family="Arial Black"),
                name=name,
                showlegend=False,
                hovertemplate=f"<b>{name}</b><br>Status: {'Ativo' if colors[name] == '#ff6b6b' else 'Idle'}<extra></extra>"
            ))
        
        # Adicionar setas (conexões)
        arrows = [
            ("📥 Entrada", "🎯 Planner"),
            ("🎯 Planner", "⚙️ Execution"),
            ("⚙️ Execution", "✅ Verification"),
            ("✅ Verification", "📤 Saída"),
            ("✅ Verification", "🎯 Planner")  # Re-planning
        ]
        
        for start, end in arrows:
            x0, y0 = positions[start]
            x1, y1 = positions[end]
            
            # Seta especial para re-planning
            if start == "✅ Verification" and end == "🎯 Planner":
                fig.add_annotation(
                    x=x1, y=y1,
                    ax=x0, ay=y0,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    arrowhead=3,
                    arrowsize=1.5,
                    arrowwidth=3,
                    arrowcolor="#ff6b6b",
                    text="🔄 Re-planning",
                    textangle=-45,
                    font=dict(size=12, color="#ff6b6b")
                )
            else:
                fig.add_annotation(
                    x=x1, y=y1,
                    ax=x0, ay=y0,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#666"
                )
        
        fig.update_layout(
            title={
                'text': "Arquitetura Multi-Agente",
                'x': 0.5,
                'font': {'size': 20, 'color': '#1f77b4'}
            },
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 6.5]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 3.5]),
            plot_bgcolor="rgba(248,249,250,0.8)",
            paper_bgcolor="white",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_agent_performance_chart(self):
        """Cria gráfico de performance dos agentes com mais detalhes"""
        agents = list(self.agents_data.keys())
        completed = [self.agents_data[agent]["tasks_completed"] for agent in agents]
        colors = ['#28a745', '#1f77b4', '#dc3545']
        
        fig = go.Figure()
        
        # Barras principais
        fig.add_trace(go.Bar(
            x=agents,
            y=completed,
            marker_color=colors,
            text=completed,
            textposition='auto',
            textfont=dict(size=14, color='white'),
            name="Tarefas Completadas",
            hovertemplate="<b>%{x}</b><br>Tarefas: %{y}<extra></extra>"
        ))
        
        # Adicionar linha de média
        if completed:
            avg = sum(completed) / len(completed)
            fig.add_hline(y=avg, line_dash="dash", line_color="red", 
                         annotation_text=f"Média: {avg:.1f}")
        
        fig.update_layout(
            title="Performance dos Agentes",
            xaxis_title="Agentes",
            yaxis_title="Tarefas Completadas",
            height=350,
            plot_bgcolor="rgba(248,249,250,0.8)",
            showlegend=False
        )
        
        return fig
    
    def create_system_metrics_chart(self):
        """Cria gráfico de métricas do sistema melhorado"""
        labels = ['✅ Concluídas', '❌ Falharam', '🔄 Em Processamento']
        values = [
            self.system_metrics["completed_tasks"],
            self.system_metrics["failed_tasks"],
            max(0, self.system_metrics["total_tasks"] - self.system_metrics["completed_tasks"] - self.system_metrics["failed_tasks"])
        ]
        colors = ['#28a745', '#dc3545', '#ffc107']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=colors,
            textinfo='label+percent+value',
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>"
        )])
        
        # Adicionar texto central
        total = sum(values)
        fig.add_annotation(
            text=f"<b>Total<br>{total}</b>",
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )
        
        fig.update_layout(
            title="Status das Tarefas",
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        return fig
    
    def create_timeline_chart(self):
        """Cria gráfico de timeline das tarefas melhorado"""
        if not self.task_history:
            return go.Figure().add_annotation(
                text="Execute algumas tarefas para ver o timeline",
                x=0.5, y=0.5, showarrow=False, font_size=16
            )
        
        df = pd.DataFrame(self.task_history)
        
        # Criar cores baseadas no status
        color_map = {
            "completed": "#28a745",
            "failed": "#dc3545", 
            "processing": "#ffc107"
        }
        
        fig = px.timeline(
            df,
            x_start="start_time",
            x_end="end_time",
            y="task_name",
            color="status",
            color_discrete_map=color_map,
            title="⏱️ Timeline de Execução das Tarefas"
        )
        
        fig.update_layout(
            height=350,
            xaxis_title="Tempo",
            yaxis_title="Tarefas",
            plot_bgcolor="rgba(248,249,250,0.8)"
        )
        
        return fig
    
    def create_real_time_metrics(self):
        """Cria métricas em tempo real"""
        metrics = self.system_metrics
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Total de Tarefas",
                metrics["total_tasks"],
                delta=1 if self.current_task else 0
            )
        
        with col2:
            st.metric(
                "✅ Taxa de Sucesso",
                f"{metrics['success_rate']:.1f}%",
                delta=f"{metrics['success_rate']:.1f}%" if metrics['total_tasks'] > 0 else "0%"
            )
        
        with col3:
            st.metric(
                "🔄 Re-planejamentos",
                metrics["replanning_events"],
                delta=1 if metrics["replanning_events"] > 0 else 0
            )
        
        with col4:
            avg_time = sum([t.get("completion_time", 0) for t in self.task_history]) / len(self.task_history) if self.task_history else 0
            st.metric(
                "⏱️ Tempo Médio",
                f"{avg_time:.1f}s",
                delta=f"{avg_time:.1f}s"
            )
    
    def simulate_task_processing(self, task_name: str, complexity: str = "medium"):
        """Simula o processamento de uma tarefa com animações melhoradas"""
        
        # Configurações baseadas na complexidade
        complexity_config = {
            "simple": {"steps": 4, "time_per_step": 0.8, "failure_chance": 0.1},
            "medium": {"steps": 6, "time_per_step": 1.2, "failure_chance": 0.2},
            "complex": {"steps": 8, "time_per_step": 1.8, "failure_chance": 0.3}
        }
        
        config = complexity_config.get(complexity, complexity_config["medium"])
        
        # Inicializar tarefa
        task_start = datetime.now()
        self.current_task = {
            "name": task_name,
            "start_time": task_start,
            "status": "processing",
            "current_agent": "Planner Agent",
            "progress": 0,
            "complexity": complexity
        }
        
        self.system_metrics["current_task"] = task_name
        
        # Log inicial
        self.add_log_entry("info", "Sistema", task_name, 
                          f"Iniciando processamento da tarefa", 
                          f"Complexidade: {complexity.upper()}, Etapas estimadas: {config['steps']}")
        
        # Container para atualizações em tempo real
        status_container = st.empty()
        progress_container = st.empty()
        details_container = st.empty()
        
        # Simular processamento
        total_steps = config["steps"]
        agents = ["Planner Agent", "Execution Agent", "Verification Agent"]
        
        replanning_occurred = False
        
        for step in range(total_steps):
            # Determinar agente atual
            if step < 2:
                current_agent = "Planner Agent"
                phase = "🎯 Planejamento"
            elif step < total_steps - 1:
                current_agent = "Execution Agent"
                phase = "⚙️ Execução"
            else:
                current_agent = "Verification Agent"
                phase = "✅ Verificação"
            
            # Atualizar status
            self.current_task["current_agent"] = current_agent
            self.current_task["progress"] = (step + 1) / total_steps
            self.agents_data[current_agent]["current_status"] = "Processing"
            
            # Gerar detalhes da execução
            execution_details = self.generate_detailed_execution_steps(current_agent, task_name, step, total_steps)
            
            # Log da etapa iniciada
            self.add_log_entry("info", current_agent, task_name,
                              f"Iniciando: {execution_details['action']}")
            
            # Mostrar progresso com mais detalhes
            with status_container.container():
                st.markdown(f"""
                <div class="task-progress">
                    <h4>🔄 {phase} - {current_agent}</h4>
                    <p><strong>Tarefa:</strong> {task_name}</p>
                    <p><strong>Complexidade:</strong> {complexity.upper()}</p>
                    <p><strong>Etapa:</strong> {step + 1}/{total_steps}</p>
                    <p><strong>Ação:</strong> {execution_details['action']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with progress_container.container():
                progress_bar = st.progress(self.current_task["progress"])
                st.write(f"**Progresso:** {self.current_task['progress']:.1%}")
            
            # Mostrar detalhes da fase atual
            with details_container.container():
                st.info(f"🔍 **Executando:** {execution_details['action']}")
            
            # Simular tempo de processamento
            time.sleep(config["time_per_step"])
            
            # Log do resultado da etapa
            self.add_log_entry("success", current_agent, task_name,
                              f"Concluído: {execution_details['action']}",
                              f"Resultado: {execution_details['result']} | {execution_details['details']}")
            
            # Chance de falha e re-planejamento
            if random.random() < config["failure_chance"] and step > 2 and not replanning_occurred:
                replanning_occurred = True
                error_scenario = self.generate_error_scenarios(current_agent, task_name)
                
                # Log do erro
                self.add_log_entry("error", current_agent, task_name,
                                  f"ERRO: {error_scenario['error']}",
                                  f"Detalhes: {error_scenario['details']}")
                
                self.system_metrics["replanning_events"] += 1
                
                with status_container.container():
                    st.warning("⚠️ **Verificação falhou** - Iniciando re-planejamento...")
                    st.markdown("🔄 **Re-planejamento em andamento...**")
                
                # Log do re-planejamento
                self.add_log_entry("warning", "Sistema", task_name,
                                  "Iniciando processo de re-planejamento",
                                  f"Solução proposta: {error_scenario['solution']}")
                
                time.sleep(2)
                
                # Log da correção
                self.add_log_entry("info", "Planner Agent", task_name,
                                  "Re-planejamento concluído",
                                  f"Plano ajustado: {error_scenario['solution']}")
                
                continue
            
            # Reset status do agente anterior
            for agent in agents:
                if agent != current_agent:
                    self.agents_data[agent]["current_status"] = "Idle"
        
        # Finalizar tarefa
        task_end = datetime.now()
        completion_time = (task_end - task_start).total_seconds()
        
        # Determinar sucesso
        success = random.random() > 0.15  # 85% chance de sucesso
        
        if success:
            status = "completed"
            self.system_metrics["completed_tasks"] += 1
            
            # Log de sucesso
            self.add_log_entry("success", "Sistema", task_name,
                              f"Tarefa concluída com sucesso!",
                              f"Tempo total: {completion_time:.1f}s, Re-planejamentos: {1 if replanning_occurred else 0}")
            
            with status_container.container():
                st.success(f"🎉 **Tarefa '{task_name}' concluída com sucesso!**")
                st.balloons()
        else:
            status = "failed"
            self.system_metrics["failed_tasks"] += 1
            
            # Gerar motivo da falha
            final_error = self.generate_error_scenarios("Verification Agent", task_name)
            
            # Log de falha
            self.add_log_entry("error", "Sistema", task_name,
                              f"Tarefa falhou após múltiplas tentativas",
                              f"Motivo final: {final_error['error']} - {final_error['details']}")
            
            with status_container.container():
                st.error(f"💥 **Tarefa '{task_name}' falhou após múltiplas tentativas**")
                st.error(f"**Motivo:** {final_error['error']}")
        
        # Atualizar métricas
        self.system_metrics["total_tasks"] += 1
        self.system_metrics["success_rate"] = (
            self.system_metrics["completed_tasks"] / self.system_metrics["total_tasks"]
        ) * 100
        
        # Atualizar agentes
        for agent in agents:
            self.agents_data[agent]["tasks_completed"] += 1
            self.agents_data[agent]["current_status"] = "Idle"
            
            # Log final do agente
            self.add_log_entry("info", agent, task_name,
                              f"Agente finalizado",
                              f"Status: {status}, Contribuição concluída")
        
        # Adicionar ao histórico
        self.task_history.append({
            "task_name": task_name,
            "start_time": task_start,
            "end_time": task_end,
            "status": status,
            "completion_time": completion_time,
            "complexity": complexity,
            "replanning_occurred": replanning_occurred
        })
        
        self.current_task = None
        self.system_metrics["current_task"] = None
        
        # Limpar containers
        time.sleep(2)
        progress_container.empty()
        details_container.empty()
        
        return status == "completed"

def main():
    """Função principal da demonstração"""
    
    # Título principal
    st.markdown('<h1 class="main-header">Sistema Multi-Agente</h1>', unsafe_allow_html=True)
    
    # Inicializar demo
    if 'demo' not in st.session_state:
        st.session_state.demo = VisualMultiAgentDemo()
    
    demo = st.session_state.demo
    
    # Seleção de tarefa
    task_options = [
        "Desenvolver API REST",
        "Criar Dashboard Analytics", 
        "Implementar Sistema de Login",
        "Integração com API Externa",
        "Sistema de Relatórios",
        "Pipeline de Machine Learning",
        "Sistema de Autenticação",
        "Módulo de Pagamentos"
    ]
    
    selected_task = st.sidebar.selectbox("Escolha uma tarefa:", task_options)
    
    complexity = st.sidebar.select_slider(
        "Complexidade:",
        options=["simple", "medium", "complex"],
        value="medium",
        format_func=lambda x: {"simple": "🟢 Simples", "medium": "🟡 Média", "complex": "🔴 Complexa"}[x]
    )
    
    # Botão para executar tarefa
    if st.sidebar.button("Executar Tarefa", type="primary"):
        with st.spinner("Processando tarefa..."):
            demo.simulate_task_processing(selected_task, complexity)
        st.rerun()
    
    # Botão para resetar métricas
    if st.sidebar.button("Resetar Sistema"):
        st.session_state.demo = VisualMultiAgentDemo()
        st.rerun()
    
    # Layout principal
    
    # Métricas em tempo real no topo
    st.markdown("## Métricas do Sistema em Tempo Real")
    demo.create_real_time_metrics()
    
    st.markdown("---")
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Diagrama da arquitetura
        st.markdown("## Arquitetura do Sistema")
        fig_arch = demo.create_architecture_diagram()
        st.plotly_chart(fig_arch, use_container_width=True)
        
        # Timeline das tarefas
        if demo.task_history:
            st.markdown("## ⏱️ Timeline de Execução")
            fig_timeline = demo.create_timeline_chart()
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Status dos agentes
        st.markdown("## Status dos Agentes")
        
        for agent_name, agent_data in demo.agents_data.items():
            is_active = demo.current_task and agent_name in demo.current_task.get("current_agent", "")
            card_class = "agent-card-active" if is_active else "agent-card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <h4>{agent_data['icon']} {agent_name}</h4>
                <p><strong>Função:</strong> {agent_data['description']}</p>
                <p><strong>Status:</strong> <span class="status-{'processing' if is_active else 'success'}">{agent_data['current_status']}</span></p>
                <p><strong>Tarefas Processadas:</strong> {agent_data['tasks_completed']}</p>
                {f'<p><strong>🔥 PROCESSANDO AGORA</strong></p>' if is_active else ''}
            </div>
            """, unsafe_allow_html=True)
    
    # Gráficos de performance
    st.markdown("---")
    st.markdown("## Análises e Performance")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if demo.system_metrics["total_tasks"] > 0:
            fig_performance = demo.create_agent_performance_chart()
            st.plotly_chart(fig_performance, use_container_width=True)
        else:
            st.info("Sem tarefas para executar")
    
    with col4:
        if demo.system_metrics["total_tasks"] > 0:
            fig_metrics = demo.create_system_metrics_chart()
            st.plotly_chart(fig_metrics, use_container_width=True)
        else:
            st.info("Sem tarefas para executar")
    
    # Seção de logs detalhados
    st.markdown("---")
    demo.display_execution_logs()

if __name__ == "__main__":
    main() 