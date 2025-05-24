from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REPLANNING = "needs_replanning"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    requirements: List[str]
    expected_output: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

@dataclass
class SubTask:
    id: str
    parent_task_id: str
    title: str
    description: str
    order: int
    status: TaskStatus
    estimated_time: int  # em minutos
    dependencies: List[str]  # IDs de outras subtarefas
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class Plan:
    id: str
    task_id: str
    subtasks: List[SubTask]
    estimated_total_time: int
    created_at: datetime
    agent_id: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now()

@dataclass
class ExecutionResult:
    id: str
    task_id: str
    subtask_id: Optional[str]
    success: bool
    output: Any
    error_message: Optional[str]
    execution_time: int  # em segundos
    timestamp: datetime
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()

@dataclass
class VerificationResult:
    id: str
    task_id: str
    passed: bool
    quality_score: float  # 0.0 a 1.0
    accuracy_score: float  # 0.0 a 1.0
    issues_found: List[str]
    recommendations: List[str]
    timestamp: datetime
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now() 