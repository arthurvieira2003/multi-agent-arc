# Sistema Multi-Agente em Python

Este projeto implementa uma arquitetura multi-agente baseada no diagrama fornecido, demonstrando como diferentes agentes especializados podem trabalhar em conjunto para processar tarefas complexas de forma coordenada.

## 🏗️ Arquitetura

O sistema é composto por três agentes principais que seguem o fluxo mostrado na imagem:

```
Requests/Tasks/Goals → Planner Agent → Execution Agent → Verification Agent → Completed Tasks
                           ↑                                      ↓
                           └─────── Re-planning ←─────────────────┘
```

### 🤖 Agentes

#### 📋 Planner Agent

- **Responsabilidade**: Quebra problemas complexos em subtarefas executáveis
- **Capacidades**:
  - Análise de complexidade de tarefas
  - Decomposição em subtarefas
  - Análise de dependências
  - Estimativa de tempo
  - Estratégias de planejamento (sequencial, paralelo, híbrido)

#### ⚙️ Execution Agent

- **Responsabilidade**: Executa as subtarefas definidas no plano
- **Capacidades**:
  - Execução de diferentes tipos de tarefas
  - Geração de código
  - Manipulação de arquivos
  - Integração com APIs
  - Operações de banco de dados
  - Execução de testes

#### ✅ Verification Agent

- **Responsabilidade**: Verifica qualidade e precisão dos resultados
- **Capacidades**:
  - Avaliação de qualidade
  - Verificação de precisão
  - Revisão de código
  - Análise de performance
  - Verificação de conformidade
  - Detecção de erros

## 🚀 Funcionalidades

- **Planejamento Inteligente**: Análise automática de complexidade e escolha de estratégia
- **Execução Coordenada**: Respeita dependências entre subtarefas
- **Verificação Automática**: Avalia qualidade e precisão dos resultados
- **Re-planejamento Adaptativo**: Ajusta planos baseado em problemas encontrados
- **Métricas Detalhadas**: Acompanha performance de agentes e sistema
- **Logging Completo**: Registra todas as atividades dos agentes

## 📁 Estrutura do Projeto

```
multi-agent-arc/
├── models.py                    # Modelos de dados (Task, Plan, Results, etc.)
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # Classe base para todos os agentes
│   ├── planner_agent.py        # Agente de planejamento
│   ├── execution_agent.py      # Agente de execução
│   └── verification_agent.py   # Agente de verificação
├── multi_agent_system.py       # Sistema principal que coordena os agentes
├── example_demo.py             # Demonstração completa do sistema
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## 🛠️ Instalação

1. **Clone o repositório**:

```bash
git clone <repository-url>
cd multi-agent-arc
```

2. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Exemplo Básico

```python
from datetime import datetime
from models import Task, TaskPriority, TaskStatus
from multi_agent_system import MultiAgentSystem

# Criar sistema multi-agente
system = MultiAgentSystem()

# Criar uma tarefa
task = Task(
    id="",
    title="Desenvolver API REST",
    description="Criar API completa para gerenciamento de usuários",
    priority=TaskPriority.HIGH,
    status=TaskStatus.PENDING,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    requirements=[
        "Endpoints CRUD",
        "Autenticação JWT",
        "Documentação",
        "Testes"
    ],
    expected_output="API funcional com documentação"
)

# Processar a tarefa
result = system.process_task(task)

# Verificar resultado
if result['status'] == 'completed':
    print(f"✅ Tarefa concluída!")
    print(f"Qualidade: {result['verification']['quality_score']:.2f}")
    print(f"Precisão: {result['verification']['accuracy_score']:.2f}")
```

### Demonstração Completa

Execute o exemplo de demonstração para ver o sistema em ação:

```bash
python example_demo.py
```

Este exemplo demonstra:

- Processamento de tarefa única
- Processamento de múltiplas tarefas
- Processo de re-planejamento
- Métricas e análises detalhadas

## 📊 Tipos de Tarefas Suportadas

O sistema pode processar diferentes tipos de tarefas:

- **Análise**: Levantamento de requisitos, análise de stakeholders
- **Design**: Arquitetura de sistema, prototipagem
- **Implementação**: Desenvolvimento de código, criação de módulos
- **Testes**: Testes unitários, integração, end-to-end
- **Documentação**: Manuais técnicos, documentação de API
- **Setup**: Configuração de ambiente, instalação de ferramentas
- **Integração**: Conexão entre módulos, APIs externas
- **Otimização**: Melhoria de performance, refatoração

## 🔄 Fluxo de Processamento

1. **Recebimento da Tarefa**: Sistema recebe uma tarefa com requisitos
2. **Planejamento**: Planner Agent analisa e cria plano de subtarefas
3. **Execução**: Execution Agent executa subtarefas respeitando dependências
4. **Verificação**: Verification Agent avalia qualidade e precisão
5. **Decisão**: Se passou na verificação → Concluído, senão → Re-planejamento
6. **Re-planejamento**: Ajusta plano baseado nos problemas encontrados
7. **Repetição**: Volta ao passo 3 até sucesso ou limite de tentativas

## 📈 Métricas e Monitoramento

O sistema coleta métricas detalhadas:

### Métricas do Sistema

- Taxa de sucesso geral
- Tempo médio de conclusão
- Taxa de re-planejamento
- Número de tarefas processadas

### Métricas dos Agentes

- Tarefas completadas por agente
- Taxa de sucesso individual
- Tempo médio de execução
- Performance histórica

### Métricas de Verificação

- Score de qualidade (0.0 - 1.0)
- Score de precisão (0.0 - 1.0)
- Problemas identificados
- Recomendações geradas

## 🎛️ Configuração

### Thresholds de Qualidade

Você pode ajustar os critérios de qualidade no `VerificationAgent`:

```python
quality_thresholds = {
    "minimum_quality_score": 0.7,
    "minimum_accuracy_score": 0.8,
    "maximum_error_rate": 0.1,
    "performance_threshold": 2.0
}
```

### Estratégias de Planejamento

O `PlannerAgent` suporta três estratégias:

- **Sequential**: Subtarefas executadas em sequência
- **Parallel**: Algumas subtarefas podem ser executadas em paralelo
- **Hybrid**: Combina abordagens sequencial e paralela para tarefas complexas

## 🧪 Testes

Para testar o sistema:

```bash
# Executar demonstração completa
python example_demo.py

# Testar componentes individuais
python -c "from agents.planner_agent import PlannerAgent; print('Planner OK')"
python -c "from agents.execution_agent import ExecutionAgent; print('Executor OK')"
python -c "from agents.verification_agent import VerificationAgent; print('Verifier OK')"
```

## 🔧 Extensibilidade

### Adicionando Novos Tipos de Execução

Para adicionar suporte a novos tipos de tarefas no `ExecutionAgent`:

```python
def _execute_new_type(self, subtask: SubTask) -> Dict[str, Any]:
    """Executa novo tipo de tarefa"""
    # Implementar lógica específica
    return {
        "type": "new_type",
        "result": "resultado da execução"
    }

# Adicionar ao dicionário de estratégias
self.execution_strategies["novo_tipo"] = self._execute_new_type
```

### Adicionando Novos Critérios de Verificação

Para adicionar novos critérios no `VerificationAgent`:

```python
def _verify_new_type(self, result: ExecutionResult) -> Dict[str, Any]:
    """Verifica novo tipo de resultado"""
    # Implementar critérios específicos
    return {
        "result_id": result.id,
        "quality_score": score,
        "accuracy_score": accuracy,
        "issues": issues,
        "type": "new_type"
    }

# Adicionar ao dicionário de critérios
self.verification_criteria["new_type"] = self._verify_new_type
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Casos de Uso

Este sistema multi-agente pode ser aplicado em diversos cenários:

- **Desenvolvimento de Software**: Automação de ciclo de desenvolvimento
- **Análise de Dados**: Pipeline de processamento e análise
- **DevOps**: Automação de deploy e monitoramento
- **Gestão de Projetos**: Decomposição e execução de projetos complexos
- **Controle de Qualidade**: Verificação automática de deliverables

## 📞 Suporte

Para dúvidas, sugestões ou problemas:

- Abra uma issue no GitHub
- Consulte a documentação dos agentes individuais
- Execute os exemplos de demonstração para entender o funcionamento
