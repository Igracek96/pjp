"""AST node definitions. Pure data containers with no logic."""

from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class Program:
    statements: List[Any]


@dataclass
class VarDecl:
    var_type: str          # "int", "float", "bool", "string"
    names: List[str]


@dataclass
class Assign:
    target: Any            # Var node
    value: Any
    type: Optional[str] = None


@dataclass
class BinOp:
    op: str
    left: Any
    right: Any
    type: Optional[str] = None


@dataclass
class UnaryOp:
    op: str                # "!" or "-"
    operand: Any
    type: Optional[str] = None


@dataclass
class IntToFloat:
    """Inserted by TypeChecker when implicit int->float conversion is needed."""
    expr: Any
    type: str = "float"


@dataclass
class If:
    condition: Any
    then_stmt: Any
    else_stmt: Optional[Any] = None


@dataclass
class While:
    condition: Any
    body: Any


@dataclass
class Block:
    statements: List[Any]


@dataclass
class Read:
    variables: List[Any]   # list of Var nodes


@dataclass
class Write:
    expressions: List[Any]


@dataclass
class Var:
    name: str
    type: Optional[str] = None


@dataclass
class IntLit:
    value: int
    type: str = "int"


@dataclass
class FloatLit:
    value: float
    type: str = "float"


@dataclass
class BoolLit:
    value: bool
    type: str = "bool"


@dataclass
class StrLit:
    value: str
    type: str = "string"


@dataclass
class ExprStmt:
    """Expression used as a statement - result is discarded."""
    expr: Any


@dataclass
class Empty:
    """Empty statement (';')."""
    pass
