class InvestigatorToolsError(Exception):
    pass

class UnknownToolError(InvestigatorToolsError):
    pass

class InvestigationLimitError(InvestigatorToolsError):
    pass