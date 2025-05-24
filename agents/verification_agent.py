from typing import List, Dict, Any, Tuple
import time
import random
from datetime import datetime

from .base_agent import BaseAgent
from models import ExecutionResult, VerificationResult, Task

class VerificationAgent(BaseAgent):
    """Agente responsável por verificar qualidade e precisão dos resultados"""
    
    def __init__(self):
        super().__init__(
            name="Verification Agent",
            capabilities=[
                "quality_assessment",
                "accuracy_verification",
                "code_review",
                "performance_analysis",
                "compliance_check",
                "error_detection"
            ]
        )
        self.quality_thresholds = {
            "minimum_quality_score": 0.7,
            "minimum_accuracy_score": 0.8,
            "maximum_error_rate": 0.1,
            "performance_threshold": 2.0  # segundos
        }
        self.verification_criteria = {
            "analysis": self._verify_analysis,
            "design": self._verify_design,
            "implementation": self._verify_implementation,
            "testing": self._verify_testing,
            "documentation": self._verify_documentation,
            "setup": self._verify_setup,
            "integration": self._verify_integration,
            "optimization": self._verify_optimization
        }
    
    def process(self, execution_results: List[ExecutionResult], task: Task) -> VerificationResult:
        """Verifica os resultados de execução e retorna avaliação de qualidade"""
        start_time = time.time()
        
        self.log_activity(f"Iniciando verificação para tarefa: {task.title}")
        
        try:
            # Verifica cada resultado individualmente
            individual_verifications = []
            for result in execution_results:
                verification = self._verify_individual_result(result)
                individual_verifications.append(verification)
            
            # Calcula scores agregados
            overall_quality = self._calculate_overall_quality(individual_verifications)
            overall_accuracy = self._calculate_overall_accuracy(individual_verifications)
            
            # Identifica problemas
            issues = self._identify_issues(individual_verifications, execution_results)
            
            # Gera recomendações
            recommendations = self._generate_recommendations(issues, individual_verifications)
            
            # Determina se passou na verificação
            passed = self._determine_pass_status(overall_quality, overall_accuracy, issues)
            
            verification_result = VerificationResult(
                id="",
                task_id=task.id,
                passed=passed,
                quality_score=overall_quality,
                accuracy_score=overall_accuracy,
                issues_found=issues,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
            execution_time = time.time() - start_time
            self.update_performance(execution_time, True)
            
            self.log_activity(
                f"Verificação concluída",
                {
                    "passed": passed,
                    "quality_score": f"{overall_quality:.2f}",
                    "accuracy_score": f"{overall_accuracy:.2f}",
                    "issues_found": len(issues)
                }
            )
            
            return verification_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.update_performance(execution_time, False)
            
            self.log_activity(f"Erro na verificação: {str(e)}")
            raise
    
    def _verify_individual_result(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica um resultado individual de execução"""
        if not result.success:
            return {
                "result_id": result.id,
                "quality_score": 0.0,
                "accuracy_score": 0.0,
                "issues": [f"Execução falhou: {result.error_message}"],
                "type": "failed_execution"
            }
        
        # Determina tipo de verificação baseado no output
        output_type = result.output.get("type", "unknown") if result.output else "unknown"
        
        if output_type in self.verification_criteria:
            return self.verification_criteria[output_type](result)
        else:
            return self._verify_generic(result)
    
    def _verify_analysis(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de análise"""
        output = result.output
        issues = []
        
        # Verifica completude da análise
        required_fields = ["requirements_identified", "stakeholders", "constraints", "risks"]
        for field in required_fields:
            if field not in output or not output[field]:
                issues.append(f"Campo obrigatório ausente ou vazio: {field}")
        
        # Verifica qualidade dos requisitos
        requirements = output.get("requirements_identified", [])
        if len(requirements) < 3:
            issues.append("Número insuficiente de requisitos identificados")
        
        # Calcula scores
        quality_score = max(0.0, 1.0 - (len(issues) * 0.2))
        accuracy_score = 0.9 if len(requirements) >= 3 else 0.6
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "analysis"
        }
    
    def _verify_design(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de design"""
        output = result.output
        issues = []
        
        # Verifica elementos essenciais do design
        if "architecture_pattern" not in output:
            issues.append("Padrão de arquitetura não especificado")
        
        components = output.get("components", [])
        if len(components) < 2:
            issues.append("Número insuficiente de componentes definidos")
        
        # Verifica se há interfaces definidas
        interfaces = output.get("interfaces", [])
        if not interfaces:
            issues.append("Interfaces não definidas")
        
        quality_score = max(0.0, 1.0 - (len(issues) * 0.25))
        accuracy_score = 0.85 if len(components) >= 3 else 0.7
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "design"
        }
    
    def _verify_implementation(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de implementação"""
        output = result.output
        issues = []
        
        # Verifica se arquivos foram criados
        files_created = output.get("files_created", [])
        if len(files_created) < 3:
            issues.append("Número insuficiente de arquivos criados")
        
        # Verifica qualidade do código
        code_quality = output.get("code_quality_score", 0.0)
        if code_quality < 0.7:
            issues.append(f"Qualidade do código baixa: {code_quality:.2f}")
        
        # Verifica linhas de código
        lines_of_code = output.get("lines_of_code", 0)
        if lines_of_code < 100:
            issues.append("Implementação muito pequena")
        
        quality_score = min(1.0, code_quality + 0.1)
        accuracy_score = 0.9 if lines_of_code >= 200 else 0.7
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "implementation"
        }
    
    def _verify_testing(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de testes"""
        output = result.output
        issues = []
        
        tests_executed = output.get("tests_executed", 0)
        tests_passed = output.get("tests_passed", 0)
        coverage = output.get("coverage_percentage", 0)
        
        # Verifica cobertura de testes
        if coverage < 80:
            issues.append(f"Cobertura de testes baixa: {coverage:.1f}%")
        
        # Verifica taxa de sucesso dos testes
        if tests_executed > 0:
            success_rate = tests_passed / tests_executed
            if success_rate < 0.9:
                issues.append(f"Taxa de sucesso dos testes baixa: {success_rate:.1%}")
        else:
            issues.append("Nenhum teste executado")
        
        # Verifica número de bugs
        bugs_found = output.get("bugs_found", 0)
        if bugs_found > 3:
            issues.append(f"Muitos bugs encontrados: {bugs_found}")
        
        quality_score = min(1.0, coverage / 100.0 + 0.1)
        accuracy_score = success_rate if tests_executed > 0 else 0.0
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "testing"
        }
    
    def _verify_documentation(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de documentação"""
        output = result.output
        issues = []
        
        documents = output.get("documents_created", [])
        if len(documents) < 2:
            issues.append("Número insuficiente de documentos criados")
        
        pages = output.get("pages_written", 0)
        if pages < 10:
            issues.append("Documentação muito breve")
        
        sections = output.get("sections", [])
        required_sections = ["Introdução", "Instalação", "Uso"]
        missing_sections = [s for s in required_sections if s not in sections]
        if missing_sections:
            issues.append(f"Seções obrigatórias ausentes: {', '.join(missing_sections)}")
        
        quality_score = max(0.0, 1.0 - (len(issues) * 0.2))
        accuracy_score = 0.9 if pages >= 20 else 0.7
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "documentation"
        }
    
    def _verify_setup(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de configuração"""
        output = result.output
        issues = []
        
        if not output.get("environment_configured", False):
            issues.append("Ambiente não configurado adequadamente")
        
        tools = output.get("tools_installed", [])
        if len(tools) < 3:
            issues.append("Ferramentas insuficientes instaladas")
        
        config_files = output.get("config_files", [])
        if not config_files:
            issues.append("Arquivos de configuração não criados")
        
        quality_score = max(0.0, 1.0 - (len(issues) * 0.3))
        accuracy_score = 0.95 if len(tools) >= 5 else 0.8
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "setup"
        }
    
    def _verify_integration(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de integração"""
        output = result.output
        issues = []
        
        modules = output.get("modules_integrated", [])
        if len(modules) < 2:
            issues.append("Número insuficiente de módulos integrados")
        
        if not output.get("data_flow_verified", False):
            issues.append("Fluxo de dados não verificado")
        
        integration_tests = output.get("integration_tests_passed", 0)
        if integration_tests < 5:
            issues.append("Testes de integração insuficientes")
        
        quality_score = max(0.0, 1.0 - (len(issues) * 0.25))
        accuracy_score = 0.9 if integration_tests >= 10 else 0.7
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "integration"
        }
    
    def _verify_optimization(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verifica resultados de otimização"""
        output = result.output
        issues = []
        
        optimizations = output.get("optimizations_applied", [])
        if len(optimizations) < 2:
            issues.append("Número insuficiente de otimizações aplicadas")
        
        improvements = output.get("performance_improvements", {})
        if not improvements:
            issues.append("Melhorias de performance não documentadas")
        
        # Verifica se houve melhoria significativa
        response_time_improvement = improvements.get("response_time", "0% faster")
        if "faster" not in response_time_improvement:
            issues.append("Tempo de resposta não melhorou")
        
        quality_score = max(0.0, 1.0 - (len(issues) * 0.2))
        accuracy_score = 0.85 if len(optimizations) >= 3 else 0.7
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "optimization"
        }
    
    def _verify_generic(self, result: ExecutionResult) -> Dict[str, Any]:
        """Verificação genérica para tipos não específicos"""
        issues = []
        
        if not result.output:
            issues.append("Resultado vazio")
        
        if result.execution_time > 300:  # 5 minutos
            issues.append("Tempo de execução muito longo")
        
        quality_score = 0.7 if not issues else 0.4
        accuracy_score = 0.6
        
        return {
            "result_id": result.id,
            "quality_score": quality_score,
            "accuracy_score": accuracy_score,
            "issues": issues,
            "type": "generic"
        }
    
    def _calculate_overall_quality(self, verifications: List[Dict[str, Any]]) -> float:
        """Calcula score de qualidade geral"""
        if not verifications:
            return 0.0
        
        total_quality = sum(v["quality_score"] for v in verifications)
        return total_quality / len(verifications)
    
    def _calculate_overall_accuracy(self, verifications: List[Dict[str, Any]]) -> float:
        """Calcula score de precisão geral"""
        if not verifications:
            return 0.0
        
        total_accuracy = sum(v["accuracy_score"] for v in verifications)
        return total_accuracy / len(verifications)
    
    def _identify_issues(self, verifications: List[Dict[str, Any]], 
                        execution_results: List[ExecutionResult]) -> List[str]:
        """Identifica todos os problemas encontrados"""
        all_issues = []
        
        # Coleta problemas individuais
        for verification in verifications:
            all_issues.extend(verification["issues"])
        
        # Verifica problemas sistêmicos
        failed_executions = [r for r in execution_results if not r.success]
        if len(failed_executions) > len(execution_results) * 0.2:
            all_issues.append("Alta taxa de falhas na execução")
        
        # Verifica tempo total de execução
        total_time = sum(r.execution_time for r in execution_results)
        if total_time > 1800:  # 30 minutos
            all_issues.append("Tempo total de execução muito longo")
        
        return list(set(all_issues))  # Remove duplicatas
    
    def _generate_recommendations(self, issues: List[str], 
                                verifications: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações baseadas nos problemas encontrados"""
        recommendations = []
        
        # Recomendações baseadas em problemas específicos
        if any("qualidade do código" in issue.lower() for issue in issues):
            recommendations.append("Implementar revisão de código mais rigorosa")
            recommendations.append("Usar ferramentas de análise estática de código")
        
        if any("cobertura" in issue.lower() for issue in issues):
            recommendations.append("Aumentar cobertura de testes para pelo menos 80%")
            recommendations.append("Implementar testes de integração adicionais")
        
        if any("documentação" in issue.lower() for issue in issues):
            recommendations.append("Expandir documentação com mais detalhes")
            recommendations.append("Adicionar exemplos práticos na documentação")
        
        if any("tempo" in issue.lower() for issue in issues):
            recommendations.append("Otimizar processos para reduzir tempo de execução")
            recommendations.append("Considerar paralelização de tarefas")
        
        # Recomendações baseadas em scores baixos
        low_quality_verifications = [v for v in verifications if v["quality_score"] < 0.7]
        if len(low_quality_verifications) > len(verifications) * 0.3:
            recommendations.append("Revisar processo de desenvolvimento para melhorar qualidade")
            recommendations.append("Implementar checkpoints de qualidade mais frequentes")
        
        if not recommendations:
            recommendations.append("Manter padrão atual de qualidade")
        
        return recommendations
    
    def _determine_pass_status(self, quality_score: float, accuracy_score: float, 
                             issues: List[str]) -> bool:
        """Determina se a verificação passou baseada nos critérios"""
        # Verifica se atende aos thresholds mínimos
        meets_quality = quality_score >= self.quality_thresholds["minimum_quality_score"]
        meets_accuracy = accuracy_score >= self.quality_thresholds["minimum_accuracy_score"]
        
        # Verifica se não há problemas críticos
        critical_issues = [
            issue for issue in issues 
            if any(keyword in issue.lower() for keyword in ["falhou", "crítico", "erro fatal"])
        ]
        
        no_critical_issues = len(critical_issues) == 0
        
        return meets_quality and meets_accuracy and no_critical_issues 