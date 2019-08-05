import io
import tokenize
from typing import List, Optional

from flake8_forbid_visual_indent import ForbidVisualIndent, ErrorPosition

Tokens = List[tokenize.TokenInfo]


def check(code: str, noqa: bool = False, error_position: Optional[ErrorPosition] = None) -> None:
    tokens = list(tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline))
    checker = ForbidVisualIndent("", "", 0, noqa, tokens[1:])
    error = next(iter(checker), None)
    if not error_position:
        assert error is None
    else:
        assert error == (error_position, ForbidVisualIndent.error_message)


class TestChecker:
    def test_noqa(self) -> None:
        check("", noqa=True)

    def test_not_enough_lines(self) -> None:
        check("x=1")

    def test_hanging_indentation(self) -> None:
        check("f(\n    1,\n    2)")

    def test_return(self) -> None:
        check("return\n    1")

    def test_multiline_function_definition(self) -> None:
        check("def func()\\\n        -> None:")

    def test_error_on_return(self) -> None:
        check("return 1 +\\\n       2", error_position=(2, 7))

    def test_error_on_comprehension(self) -> None:
        check("return [x for x in\n        l]", error_position=(2, 8))

    def test_error_on_import(self) -> None:
        check("from . import (first,\n               second)", error_position=(2, 15))

    def test_error_on_dict_comprehention(self) -> None:
        check("return {k: v\n        for k, v in l}", error_position=(2, 8))

    def test_error_on_map(self) -> None:
        check("map(f,\n    l)", error_position=(2, 4))
