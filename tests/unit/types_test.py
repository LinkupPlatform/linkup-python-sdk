from typing import Any

import pydantic
import pytest

import linkup


@pytest.mark.parametrize(
    "task_input",
    [
        pytest.param(
            lambda: linkup.SearchTaskInput(
                query="query",
                depth="standard",
                output_type="structured",
            ),
            id="search",
        ),
        pytest.param(
            lambda: linkup.ResearchTaskInput(
                query="query",
                output_type="structured",
            ),
            id="research",
        ),
    ],
)
def test_structured_task_input_requires_schema(task_input: Any) -> None:  # noqa: ANN401
    with pytest.raises(
        pydantic.ValidationError,
        match="structured_output_schema must be provided",
    ):
        task_input()
