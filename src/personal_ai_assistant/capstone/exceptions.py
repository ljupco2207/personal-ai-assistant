class AssistantError(Exception):
    pass


class ProviderError(AssistantError):
    pass


class StorageError(AssistantError):
    pass


class ProviderAuthenticationError(ProviderError):
    pass


class ProviderRateLimitError(ProviderError):
    pass


class ProviderConnectionError(ProviderError):
    pass


class ProviderServerError(ProviderError):
    pass
