class IntegrationError(Exception):
    pass

class LogsUnavailableError(IntegrationError):
    pass

class MetricsUnavailableError(IntegrationError):
    pass

class DeploymentssUnavailableError(IntegrationError):
    pass