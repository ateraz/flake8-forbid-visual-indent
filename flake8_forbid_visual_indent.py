import tokenize
from itertools import groupby
from typing import Iterator, List, Tuple

__version__ = "0.0.2"


def _get_line(token: tokenize.TokenInfo) -> int:
    return token.start[0]


def _get_column(token: tokenize.TokenInfo) -> int:
    return token.start[1]


def _is_non_empty(token: tokenize.TokenInfo) -> bool:
    value = token.string
    return bool(value) and not value.isspace()


_allow_extra_indent_after = {"(", "and", "or"}
ErrorPosition = Tuple[int, int]
ErrorMessage = Tuple[ErrorPosition, str]


class ForbidVisualIndent:
    name = "flake8-forbid-visual-indent"
    version = __version__
    error_message = f"VI101 ({name}) visual indentation is not allowed"

    def __init__(
            self, logical_line: str, indent_char: str, line_number: int,
            noqa: bool, tokens: List[tokenize.TokenInfo]) -> None:
        self._messages: List[ErrorMessage] = []
        if noqa or not tokens:
            return

        first_line = _get_line(tokens[0])
        last_line = _get_line(tokens[-1])
        number_of_lines = last_line - first_line + 1
        if number_of_lines == 1:
            return

        non_empty_tokens = [token for token in tokens if _is_non_empty(token)]
        line_tokens = [list(ts) for _, ts in groupby(non_empty_tokens, _get_line)]
        if len(line_tokens) < 2:
            return

        last_token_on_first_line = line_tokens[0][-1]
        first_token_on_second_line = line_tokens[1][0]
        if first_token_on_second_line.type not in {tokenize.NAME, tokenize.NUMBER, tokenize.STRING}:
            return
        if last_token_on_first_line.string == ",":
            self._messages.append((
                first_token_on_second_line.start, self.error_message))
            return

        allowed_indents = {4}
        if last_token_on_first_line.string in _allow_extra_indent_after:
            allowed_indents.add(8)

        first_token_on_first_line = line_tokens[0][0]
        first_column_in_first_line = _get_column(first_token_on_first_line)
        first_column_in_second_line = _get_column(first_token_on_second_line)

        second_line_indent = first_column_in_second_line - first_column_in_first_line
        if second_line_indent not in allowed_indents:
            self._messages.append((
                first_token_on_second_line.start, self.error_message))

    def __iter__(self) -> Iterator[ErrorMessage]:
        return iter(self._messages)
