"""
DSLレクサー（字句解析器）

テキストをトークンに分解します。
これはインタプリタの最初のステップです。

例:
    "move player 5 3" → [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3), EOF]
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable


class TokenType(Enum):
    """トークンの種類"""

    # キーワード
    MOVE = "move"
    SPAWN = "spawn"
    DESTROY = "destroy"
    SET = "set"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    AND = "and"
    OR = "or"
    NOT = "not"
    TRUE = "true"
    FALSE = "false"

    # リテラル
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # 記号
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    COLON = ":"
    DOT = "."
    EQUALS = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQ = "=="
    NE = "!="

    # 特殊
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()


# キーワードのマッピング
KEYWORDS: dict[str, TokenType] = {
    "move": TokenType.MOVE,
    "spawn": TokenType.SPAWN,
    "destroy": TokenType.DESTROY,
    "set": TokenType.SET,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}


@dataclass(frozen=True)
class Token:
    """
    トークン

    ソースコードの最小単位を表します。
    位置情報（行、列）を持ちます。
    """

    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        if self.type in (TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER):
            return f"Token({self.type.name}, {self.value!r})"
        return f"Token({self.type.name})"


@dataclass
class LexerError:
    """レクサーエラー（警告）"""

    message: str
    line: int
    column: int
    char: str


class Lexer:
    """
    字句解析器

    ソースコードをトークンのリストに変換します。
    """

    def __init__(
        self,
        source: str,
        on_error: Callable[[LexerError], None] | None = None,
    ) -> None:
        """
        Args:
            source: ソースコード
            on_error: エラーハンドラ（Noneの場合は無視）
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.on_error = on_error
        self.errors: list[LexerError] = []

    @property
    def current_char(self) -> str | None:
        """現在の文字（終端ならNone）"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek(self, offset: int = 1) -> str | None:
        """先読み"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> str | None:
        """1文字進める"""
        char = self.current_char
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace(self) -> None:
        """空白をスキップ"""
        while self.current_char and self.current_char in " \t\r":
            self.advance()

    def skip_comment(self) -> Token | None:
        """コメントをスキップし、コメントトークンを返す"""
        if self.current_char != "#":
            return None

        start_line = self.line
        start_column = self.column
        content = ""

        self.advance()  # '#' をスキップ
        while self.current_char and self.current_char != "\n":
            content += self.current_char
            self.advance()

        return Token(TokenType.COMMENT, content.strip(), start_line, start_column)

    def read_number(self) -> Token:
        """数値を読み取る"""
        start_line = self.line
        start_column = self.column
        value = ""

        while self.current_char and self.current_char.isdigit():
            value += self.current_char
            self.advance()

        # 小数点
        if self.current_char == "." and self.peek() and self.peek().isdigit():
            value += self.current_char
            self.advance()
            while self.current_char and self.current_char.isdigit():
                value += self.current_char
                self.advance()

        return Token(TokenType.NUMBER, value, start_line, start_column)

    def read_string(self) -> Token:
        """文字列を読み取る"""
        start_line = self.line
        start_column = self.column
        quote = self.current_char
        self.advance()  # 開始クォートをスキップ

        value = ""
        while self.current_char and self.current_char != quote:
            if self.current_char == "\n":
                # 改行で文字列が終了（エラー扱い）
                self._error(f"Unterminated string at line {start_line}")
                break
            value += self.current_char
            self.advance()

        if self.current_char == quote:
            self.advance()  # 終了クォートをスキップ

        return Token(TokenType.STRING, value, start_line, start_column)

    def read_identifier(self) -> Token:
        """識別子/キーワードを読み取る"""
        start_line = self.line
        start_column = self.column
        value = ""

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            value += self.current_char
            self.advance()

        # キーワードかチェック
        token_type = KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        return Token(token_type, value, start_line, start_column)

    def read_operator(self) -> Token | None:
        """演算子/記号を読み取る"""
        start_line = self.line
        start_column = self.column
        char = self.current_char

        # 2文字演算子をチェック
        if char and self.peek():
            two_char = char + self.peek()
            two_char_ops = {
                "<=": TokenType.LE,
                ">=": TokenType.GE,
                "==": TokenType.EQ,
                "!=": TokenType.NE,
            }
            if two_char in two_char_ops:
                self.advance()
                self.advance()
                return Token(two_char_ops[two_char], two_char, start_line, start_column)

        # 1文字演算子
        one_char_ops = {
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            "{": TokenType.LBRACE,
            "}": TokenType.RBRACE,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            ".": TokenType.DOT,
            "=": TokenType.EQUALS,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "<": TokenType.LT,
            ">": TokenType.GT,
        }
        if char in one_char_ops:
            self.advance()
            return Token(one_char_ops[char], char, start_line, start_column)

        return None

    def _error(self, message: str) -> None:
        """エラーを記録"""
        error = LexerError(
            message=message,
            line=self.line,
            column=self.column,
            char=self.current_char or "",
        )
        self.errors.append(error)
        if self.on_error:
            self.on_error(error)

    def tokenize(self) -> list[Token]:
        """
        ソースコードをトークンリストに変換する

        Returns:
            トークンのリスト（最後にEOFトークン）
        """
        tokens: list[Token] = []

        while self.current_char is not None:
            # 空白をスキップ
            self.skip_whitespace()

            if self.current_char is None:
                break

            # 改行
            if self.current_char == "\n":
                tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                self.advance()
                continue

            # コメント
            if self.current_char == "#":
                comment = self.skip_comment()
                if comment:
                    tokens.append(comment)
                continue

            # 数値
            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue

            # 文字列
            if self.current_char in ('"', "'"):
                tokens.append(self.read_string())
                continue

            # 識別子/キーワード
            if self.current_char.isalpha() or self.current_char == "_":
                tokens.append(self.read_identifier())
                continue

            # 演算子/記号
            op_token = self.read_operator()
            if op_token:
                tokens.append(op_token)
                continue

            # 不明な文字（スキップして警告）
            self._error(f"Unknown character: {self.current_char!r}")
            self.advance()

        # EOF
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens


def tokenize(source: str) -> list[Token]:
    """
    ソースコードをトークンリストに変換する（簡易関数）

    Args:
        source: ソースコード

    Returns:
        トークンのリスト
    """
    lexer = Lexer(source)
    return lexer.tokenize()


def tokenize_with_errors(
    source: str,
) -> tuple[list[Token], list[LexerError]]:
    """
    ソースコードをトークンリストに変換し、エラーも返す

    Args:
        source: ソースコード

    Returns:
        (トークンリスト, エラーリスト)
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    return tokens, lexer.errors
