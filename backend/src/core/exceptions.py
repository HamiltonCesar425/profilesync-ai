"""
Exceções de domínio da aplicação.

Este módulo centraliza as exceções utilizadas pelos serviços do
ProfileSync AI, evitando o vazamento de exceções de bibliotecas
externas para as camadas superiores da aplicação.
"""


class DomainError(Exception):
    """Classe base para exceções de domínio."""


class ResourceNotFoundError(DomainError):
    """Recurso solicitado não foi encontrado."""


class BusinessRuleViolationError(DomainError):
    """Violação de regra de negócio."""


class AIAssistantError(DomainError):
    """Classe base para exceções do assistente de IA."""


class AIProviderError(AIAssistantError):
    """Erro retornado pelo provedor de IA."""


class AIProviderUnavailableError(AIProviderError):
    """O provedor de IA está temporariamente indisponível."""


class AIResponseError(AIProviderError):
    """O provedor retornou uma resposta inválida."""


class AIConfigurationError(AIAssistantError):
    """Configuração inválida da integração com IA."""
