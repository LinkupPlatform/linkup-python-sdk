from ._client import LinkupClient
from ._errors import (
    LinkupAuthenticationError,
    LinkupBudgetLimitExceededError,
    LinkupFailedFetchError,
    LinkupFetchResponseTooLargeError,
    LinkupFetchUnsupportedContentTypeError,
    LinkupFetchUrlIsFileError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
    LinkupPaymentRequiredError,
    LinkupTaskNotFoundError,
    LinkupTasksQueueLimitExceededError,
    LinkupTimeoutError,
    LinkupTooManyRequestsError,
    LinkupUnknownError,
)
from ._types import (
    LinkupFetchImageExtraction,
    LinkupFetchResponse,
    LinkupFetchTask,
    LinkupFetchTaskInput,
    LinkupResearchTask,
    LinkupResearchTaskInput,
    LinkupResearchTasksPage,
    LinkupSearchImageResult,
    LinkupSearchResults,
    LinkupSearchStructuredResponse,
    LinkupSearchTask,
    LinkupSearchTaskInput,
    LinkupSearchTextResult,
    LinkupSource,
    LinkupSourcedAnswer,
    LinkupTask,
    LinkupTaskInput,
    LinkupTaskMetadata,
    LinkupTaskQuota,
    LinkupTasksPage,
)
from ._version import __version__

# Aliases to allow usage like `import linkup` and `client = linkup.Client(...)`
AuthenticationError = LinkupAuthenticationError
BudgetLimitExceededError = LinkupBudgetLimitExceededError
Client = LinkupClient
FailedFetchError = LinkupFailedFetchError
FetchImageExtraction = LinkupFetchImageExtraction
FetchResponse = LinkupFetchResponse
FetchResponseTooLargeError = LinkupFetchResponseTooLargeError
FetchUnsupportedContentTypeError = LinkupFetchUnsupportedContentTypeError
FetchTask = LinkupFetchTask
FetchTaskInput = LinkupFetchTaskInput
FetchUrlIsFileError = LinkupFetchUrlIsFileError
InsufficientCreditError = LinkupInsufficientCreditError
InvalidRequestError = LinkupInvalidRequestError
NoResultError = LinkupNoResultError
PaymentRequiredError = LinkupPaymentRequiredError
ResearchTask = LinkupResearchTask
ResearchTaskInput = LinkupResearchTaskInput
ResearchTasksPage = LinkupResearchTasksPage
SearchImageResult = LinkupSearchImageResult
SearchResults = LinkupSearchResults
SearchStructuredResponse = LinkupSearchStructuredResponse
SearchTask = LinkupSearchTask
SearchTaskInput = LinkupSearchTaskInput
SearchTextResult = LinkupSearchTextResult
Source = LinkupSource
SourcedAnswer = LinkupSourcedAnswer
Task = LinkupTask
TaskNotFoundError = LinkupTaskNotFoundError
TaskInput = LinkupTaskInput
TaskMetadata = LinkupTaskMetadata
TaskQuota = LinkupTaskQuota
TasksPage = LinkupTasksPage
TasksQueueLimitExceededError = LinkupTasksQueueLimitExceededError
TimeoutError = LinkupTimeoutError  # noqa: A001
TooManyRequestsError = LinkupTooManyRequestsError
UnknownError = LinkupUnknownError

__all__ = [
    "AuthenticationError",
    "BudgetLimitExceededError",
    "Client",
    "FailedFetchError",
    "FetchImageExtraction",
    "FetchResponse",
    "FetchResponseTooLargeError",
    "FetchTask",
    "FetchTaskInput",
    "FetchUnsupportedContentTypeError",
    "FetchUrlIsFileError",
    "InsufficientCreditError",
    "InvalidRequestError",
    "LinkupAuthenticationError",
    "LinkupBudgetLimitExceededError",
    "LinkupClient",
    "LinkupFailedFetchError",
    "LinkupFetchImageExtraction",
    "LinkupFetchResponse",
    "LinkupFetchResponseTooLargeError",
    "LinkupFetchTask",
    "LinkupFetchTaskInput",
    "LinkupFetchUnsupportedContentTypeError",
    "LinkupFetchUrlIsFileError",
    "LinkupInsufficientCreditError",
    "LinkupInvalidRequestError",
    "LinkupNoResultError",
    "LinkupPaymentRequiredError",
    "LinkupResearchTask",
    "LinkupResearchTaskInput",
    "LinkupResearchTasksPage",
    "LinkupSearchImageResult",
    "LinkupSearchResults",
    "LinkupSearchStructuredResponse",
    "LinkupSearchTask",
    "LinkupSearchTaskInput",
    "LinkupSearchTextResult",
    "LinkupSource",
    "LinkupSourcedAnswer",
    "LinkupTask",
    "LinkupTaskInput",
    "LinkupTaskMetadata",
    "LinkupTaskNotFoundError",
    "LinkupTaskQuota",
    "LinkupTasksPage",
    "LinkupTasksQueueLimitExceededError",
    "LinkupTimeoutError",
    "LinkupTooManyRequestsError",
    "LinkupUnknownError",
    "NoResultError",
    "PaymentRequiredError",
    "ResearchTask",
    "ResearchTaskInput",
    "ResearchTasksPage",
    "SearchImageResult",
    "SearchResults",
    "SearchStructuredResponse",
    "SearchTask",
    "SearchTaskInput",
    "SearchTextResult",
    "Source",
    "SourcedAnswer",
    "Task",
    "TaskInput",
    "TaskMetadata",
    "TaskNotFoundError",
    "TaskQuota",
    "TasksPage",
    "TasksQueueLimitExceededError",
    "TimeoutError",
    "TooManyRequestsError",
    "UnknownError",
    "__version__",
]
