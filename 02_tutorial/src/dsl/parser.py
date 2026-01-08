"""
DSLパーサー（構文解析器）

トークンをAST（抽象構文木）に変換します。
これはインタプリタの2番目のステップです。

例:
    Tokens: [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3)]
    AST: MoveCommand(target="player", x=5, y=3)
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from src.dsl.lexer import Token, TokenType, tokenize


# ============================================
# AST ノード定義
# ============================================


@dataclass
class ASTNode:
    """AST基底クラス"""

    pass


@dataclass
class MoveCommand(ASTNode):
    """移動コマンド: move <entity> <x> <y>"""

    target: str
    x: int
    y: int


@dataclass
class SpawnCommand(ASTNode):
    """生成コマンド: spawn <type> <x> <y>"""

    entity_type: str
    x: int
    y: int
    name: str = ""


@dataclass
class DestroyCommand(ASTNode):
    """削除コマンド: destroy <entity>"""

    target: str


@dataclass
class SetCommand(ASTNode):
    """設定コマンド: set <entity>.<property> <value>"""

    target: str
    property: str
    value: Any


@dataclass
class Expression(ASTNode):
    """式（基底クラス）"""

    pass


@dataclass
class NumberLiteral(Expression):
    """数値リテラル"""

    value: float


@dataclass
class StringLiteral(Expression):
    """文字列リテラル"""

    value: str


@dataclass
class BoolLiteral(Expression):
    """真偽値リテラル"""

    value: bool


@dataclass
class Identifier(Expression):
    """識別子"""

    name: str


@dataclass
class PropertyAccess(Expression):
    """プロパティアクセス: entity.property"""

    object: str
    property: str


@dataclass
class BinaryOp(Expression):
    """二項演算: left op right"""

    left: Expression
    op: str
    right: Expression


@dataclass
class UnaryOp(Expression):
    """単項演算: op operand"""

    op: str
    operand: Expression


@dataclass
class IfStatement(ASTNode):
    """条件文: if <condition> then <action> [else <action>]"""

    condition: Expression
    then_action: ASTNode
    else_action: ASTNode | None = None


@dataclass
class Program(ASTNode):
    """プログラム全体"""

    statements: list[ASTNode] = field(default_factory=list)


# ============================================
# パーサーエラー
# ============================================


@dataclass
class ParseError:
    """パースエラー"""

    message: str
    line: int
    column: int


# ============================================
# パーサー
# ============================================


class Parser:
    """
    構文解析器

    トークンリストをASTに変換します。
    """

    def __init__(
        self,
        tokens: list[Token],
        on_error: Callable[[ParseError], None] | None = None,
    ) -> None:
        """
        Args:
            tokens: トークンリスト
            on_error: エラーハンドラ
        """
        # コメントと改行を除去
        self.tokens = [
            t for t in tokens if t.type not in (TokenType.COMMENT, TokenType.NEWLINE)
        ]
        self.pos = 0
        self.on_error = on_error
        self.errors: list[ParseError] = []

    @property
    def current_token(self) -> Token:
        """現在のトークン"""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]

    def peek(self, offset: int = 0) -> Token:
        """先読み"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]

    def advance(self) -> Token:
        """1トークン進める"""
        token = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def check(self, *types: TokenType) -> bool:
        """現在のトークンが指定型かチェック"""
        return self.current_token.type in types

    def match(self, *types: TokenType) -> Token | None:
        """指定型なら消費して返す"""
        if self.check(*types):
            return self.advance()
        return None

    def consume(self, expected: TokenType, message: str = "") -> Token:
        """指定型を消費（違えばエラー）"""
        if self.check(expected):
            return self.advance()
        msg = message or f"Expected {expected.name}, got {self.current_token.type.name}"
        self._error(msg)
        return self.current_token

    def _error(self, message: str) -> None:
        """エラーを記録"""
        token = self.current_token
        error = ParseError(message=message, line=token.line, column=token.column)
        self.errors.append(error)
        if self.on_error:
            self.on_error(error)

    def synchronize(self) -> None:
        """エラー回復：次のコマンド開始まで進む"""
        self.advance()
        while not self.check(TokenType.EOF):
            # コマンド開始キーワードを見つける
            if self.check(
                TokenType.MOVE,
                TokenType.SPAWN,
                TokenType.DESTROY,
                TokenType.SET,
                TokenType.IF,
            ):
                return
            self.advance()

    # ============================================
    # 式のパース
    # ============================================

    def parse_primary(self) -> Expression:
        """基本式をパース"""
        # 数値
        if self.check(TokenType.NUMBER):
            token = self.advance()
            value = float(token.value) if "." in token.value else int(token.value)
            return NumberLiteral(value=value)

        # 文字列
        if self.check(TokenType.STRING):
            token = self.advance()
            return StringLiteral(value=token.value)

        # 真偽値
        if self.check(TokenType.TRUE):
            self.advance()
            return BoolLiteral(value=True)
        if self.check(TokenType.FALSE):
            self.advance()
            return BoolLiteral(value=False)

        # 識別子（プロパティアクセスの可能性）
        if self.check(TokenType.IDENTIFIER):
            token = self.advance()
            name = token.value

            # プロパティアクセス: entity.property
            if self.check(TokenType.DOT):
                self.advance()
                prop = self.consume(TokenType.IDENTIFIER, "Expected property name")
                return PropertyAccess(object=name, property=prop.value)

            return Identifier(name=name)

        # 括弧
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return expr

        # NOT演算子
        if self.check(TokenType.NOT):
            self.advance()
            operand = self.parse_primary()
            return UnaryOp(op="not", operand=operand)

        self._error(f"Unexpected token: {self.current_token.type.name}")
        return Identifier(name="<error>")

    def parse_comparison(self) -> Expression:
        """比較式をパース"""
        left = self.parse_primary()

        while self.check(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE, TokenType.EQ, TokenType.NE):
            op_token = self.advance()
            right = self.parse_primary()
            left = BinaryOp(left=left, op=op_token.value, right=right)

        return left

    def parse_and(self) -> Expression:
        """AND式をパース"""
        left = self.parse_comparison()

        while self.check(TokenType.AND):
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left=left, op="and", right=right)

        return left

    def parse_or(self) -> Expression:
        """OR式をパース"""
        left = self.parse_and()

        while self.check(TokenType.OR):
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left=left, op="or", right=right)

        return left

    def parse_expression(self) -> Expression:
        """式をパース"""
        return self.parse_or()

    # ============================================
    # コマンドのパース
    # ============================================

    def parse_move(self) -> MoveCommand:
        """move <entity> <x> <y>"""
        self.consume(TokenType.MOVE)
        target = self.consume(TokenType.IDENTIFIER, "Expected entity name").value
        x = int(self.consume(TokenType.NUMBER, "Expected x coordinate").value)
        y = int(self.consume(TokenType.NUMBER, "Expected y coordinate").value)
        return MoveCommand(target=target, x=x, y=y)

    def parse_spawn(self) -> SpawnCommand:
        """spawn <type> <x> <y> [<name>]"""
        self.consume(TokenType.SPAWN)
        entity_type = self.consume(TokenType.IDENTIFIER, "Expected entity type").value
        x = int(self.consume(TokenType.NUMBER, "Expected x coordinate").value)
        y = int(self.consume(TokenType.NUMBER, "Expected y coordinate").value)

        name = ""
        if self.check(TokenType.STRING):
            name = self.advance().value
        elif self.check(TokenType.IDENTIFIER):
            name = self.advance().value

        return SpawnCommand(entity_type=entity_type, x=x, y=y, name=name)

    def parse_destroy(self) -> DestroyCommand:
        """destroy <entity>"""
        self.consume(TokenType.DESTROY)
        target = self.consume(TokenType.IDENTIFIER, "Expected entity name").value
        return DestroyCommand(target=target)

    def parse_set(self) -> SetCommand:
        """set <entity>.<property> <value>"""
        self.consume(TokenType.SET)
        target = self.consume(TokenType.IDENTIFIER, "Expected entity name").value
        self.consume(TokenType.DOT, "Expected '.'")
        property_name = self.consume(TokenType.IDENTIFIER, "Expected property name").value

        # 値をパース
        value: Any
        if self.check(TokenType.NUMBER):
            token = self.advance()
            value = float(token.value) if "." in token.value else int(token.value)
        elif self.check(TokenType.STRING):
            value = self.advance().value
        elif self.check(TokenType.TRUE):
            self.advance()
            value = True
        elif self.check(TokenType.FALSE):
            self.advance()
            value = False
        else:
            value = self.consume(TokenType.IDENTIFIER).value

        return SetCommand(target=target, property=property_name, value=value)

    def parse_if(self) -> IfStatement:
        """if <condition> then <action> [else <action>]"""
        self.consume(TokenType.IF)
        condition = self.parse_expression()
        self.consume(TokenType.THEN, "Expected 'then'")
        then_action = self.parse_statement()

        else_action = None
        if self.check(TokenType.ELSE):
            self.advance()
            else_action = self.parse_statement()

        return IfStatement(
            condition=condition, then_action=then_action, else_action=else_action
        )

    def parse_statement(self) -> ASTNode:
        """文をパース"""
        if self.check(TokenType.MOVE):
            return self.parse_move()
        elif self.check(TokenType.SPAWN):
            return self.parse_spawn()
        elif self.check(TokenType.DESTROY):
            return self.parse_destroy()
        elif self.check(TokenType.SET):
            return self.parse_set()
        elif self.check(TokenType.IF):
            return self.parse_if()
        else:
            self._error(f"Unknown command: {self.current_token.value}")
            self.synchronize()
            return ASTNode()

    def parse(self) -> Program:
        """プログラム全体をパース"""
        statements: list[ASTNode] = []

        while not self.check(TokenType.EOF):
            try:
                stmt = self.parse_statement()
                statements.append(stmt)
            except Exception as e:
                self._error(str(e))
                self.synchronize()

        return Program(statements=statements)


# ============================================
# 簡易関数
# ============================================


def parse(source: str) -> Program:
    """
    ソースコードをパースする（簡易関数）

    Args:
        source: DSLソースコード

    Returns:
        ASTプログラム
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def parse_with_errors(source: str) -> tuple[Program, list[ParseError]]:
    """
    ソースコードをパースし、エラーも返す

    Args:
        source: DSLソースコード

    Returns:
        (ASTプログラム, エラーリスト)
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse()
    return program, parser.errors
