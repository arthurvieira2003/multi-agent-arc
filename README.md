# 🤖 Sistema Multi-Agente - Demonstração Visual

Uma demonstração interativa e educativa de um sistema multi-agente com interface web moderna, desenvolvida para apresentações acadêmicas.

## ✨ Funcionalidades Principais

### 🎯 Sistema Multi-Agente Completo

- **Planner Agent** 🎯: Analisa e decompõe tarefas complexas
- **Execution Agent** ⚙️: Executa as subtarefas do plano
- **Verification Agent** ✅: Verifica qualidade e precisão dos resultados

### 📊 Interface Visual Interativa

- **Diagrama da Arquitetura**: Visualização em tempo real dos agentes ativos
- **Métricas Dinâmicas**: Taxa de sucesso, tempo médio, re-planejamentos
- **Gráficos Interativos**: Performance dos agentes e status das tarefas
- **Timeline de Execução**: Histórico visual das tarefas processadas

### 📋 Sistema de Logs Detalhados

- **Logs em Tempo Real**: Registro de todas as etapas de execução
- **Detalhes de Processamento**: Ações específicas, resultados e retornos
- **Cenários de Erro Realistas**: Simulação de falhas com motivos detalhados
- **Filtros Avançados**: Por nível (sucesso, erro, aviso, info) e agente
- **Estatísticas dos Logs**: Contadores e métricas dos eventos registrados

### 🎬 Execução Manual Intuitiva

- **Seleção de Tarefas**: 8 tipos diferentes de tarefas para demonstrar
- **Controle de Complexidade**: Simples, Média ou Complexa
- **Processamento Visual**: Acompanhe cada etapa em tempo real
- **Animações CSS**: Efeitos visuais para destacar agentes ativos

## 🏗️ Arquitetura

O sistema demonstra o fluxo de trabalho de um sistema multi-agente:

```
📥 Entrada → 🎯 Planner → ⚙️ Execution → ✅ Verification → 📤 Saída
              ↑                                    ↓
              └─────── 🔄 Re-planning ←─────────────┘
```

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install streamlit plotly pandas
```

### Executar a Demonstração Web

```bash
streamlit run visual_demo.py
```

## 🔍 Logs Detalhados

### O que é registrado:

- **Início de cada etapa**: Ação específica sendo executada
- **Resultados detalhados**: Retornos realistas de cada operação
- **Erros e falhas**: Motivos específicos com detalhes técnicos
- **Soluções aplicadas**: Como o sistema resolve problemas
- **Métricas de tempo**: Duração de cada fase

### Exemplos de logs:

```
✅ [19:43:18] Planner Agent → Desenvolver API REST
   📄 Concluído: Análise inicial da tarefa
   🔍 Resultado: Tarefa classificada como complexidade MÉDIA |
       Identificados 4 módulos principais necessários

❌ [19:43:20] Execution Agent → Criar Dashboard Analytics
   📄 ERRO: Falha na conexão com API externa
   🔍 Detalhes: API de pagamentos retornou erro 503 - Service Unavailable

⚠️ [19:43:20] Sistema → Criar Dashboard Analytics
   📄 Iniciando processo de correção
   🔍 Solução aplicada: Implementação de retry com backoff exponencial
```

### Filtros disponíveis:

- **Por nível**: Sucessos, erros, avisos, informações
- **Por agente**: Planner, Execution, Verification, Sistema
- **Limpeza**: Botão para resetar todos os logs

## 📁 Estrutura do Projeto

```
multi-agent-arc/
├── visual_demo.py           # Demonstração web principal
├── requirements.txt         # Dependências
└── README.md               # Este arquivo (documentação completa)
```

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Interface web interativa
- **Plotly**: Gráficos e visualizações dinâmicas
- **Pandas**: Manipulação de dados
- **Python**: Lógica do sistema multi-agente

## 🧪 Testando o Sistema

### Teste Completo da Interface Web

```bash
streamlit run visual_demo.py
```

### Verificar Dependências

```bash
python -c "import streamlit, plotly, pandas; print('✅ Todas as dependências OK!')"
```

## 👥 Autores

**Acadêmicos:**

- **Arthur Henrique Tscha Vieira**
- **Rafael Rodrigues Ferreira de Andrade**
