class AssistantError(Exception):
    pass

class ProviderError(AssistantError):
    pass

class StorageError(AssistantError):
    pass