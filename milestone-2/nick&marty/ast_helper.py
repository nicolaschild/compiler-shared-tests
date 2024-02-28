"""This visitor creates a way to test the depth and precedence of AST nodes."""

# Import abstract visitor
from submodules.visitor.visitor import Visitor  # type: ignore
# Import your node types or it will not work.


class AstTestVisitor(Visitor):
    """Visitor that tests the AST structure."""

    def __init__(self) -> None:
        self.stack: list[str] = []
        self.indent_level = 0
        self.output_ast = ""

    def indent(self) -> str:
        return "-" * self.indent_level

    # -- CHILDREN
    def visit_identifier(self, identifier: Identifier) -> None:
        self.output_ast += f"{self.indent()}ID: {identifier.name}\n"

    def visit_bool_literal(self, bool_literal: BoolLiteral) -> None:
        self.output_ast += f"{self.indent()}Bool: {bool_literal.value}\n"

    def visit_int_literal(self, int_literal: IntLiteral) -> None:
        self.output_ast += f"{self.indent()}Int: {int_literal.value}\n"

    def visit_string_literal(self, string_literal: StringLiteral) -> None:
        self.output_ast += f"{self.indent()}String: {string_literal.value}\n"

    def visit_char_literal(self, char_literal: CharLiteral) -> None:
        self.output_ast += f"{self.indent()}Char: {char_literal.value}\n"

    def visit_this_literal(self, this_literal: ThisLiteral) -> None:
        self.output_ast += f"{self.indent()}this\n"

    def visit_null_literal(self, null_literal: NullLiteral) -> None:
        self.output_ast += f"{self.indent()}null\n"

    def visit_break_statement(self, break_statement: BreakStatement) -> None:
        self.output_ast += f"{self.indent()}break\n"

    # --PARENTS
    def pre_visit_type(self, type: Type) -> None:
        self.output_ast += f"{self.indent()}Type\n"
        self.indent_level += 1

    def visit_type(self, type: Type) -> None:
        self.indent_level -= 1

    def pre_visit_index(self, index: Index) -> None:
        self.output_ast += f"{self.indent()}Index\n"
        self.indent_level += 1

    def visit_index(self, index: Index) -> None:
        self.indent_level -= 1

    def pre_visit_array(self, array: Array) -> None:
        self.output_ast += f"{self.indent()}Array\n"
        self.indent_level += 1

    def visit_array(self, array: Array) -> None:
        self.indent_level -= 1

    def pre_visit_parameter(self, parameter: Parameter) -> None:
        self.output_ast += f"{self.indent()}Parameter\n"
        self.indent_level += 1

    def visit_parameter(self, parameter: Parameter) -> None:
        self.indent_level -= 1

    def pre_visit_variable_declaration(
        self, variable_declaration: VariableDeclaration
    ) -> None:
        self.output_ast += f"{self.indent()}VariableDeclaration\n"
        self.indent_level += 1

    def visit_variable_declaration(
        self, variable_declaration: VariableDeclaration
    ) -> None:
        self.indent_level -= 1

    def pre_visit_unary_operation(self, unary_operation: UnaryOperation) -> None:
        self.output_ast += f"{self.indent()}UnaryOp: {unary_operation.operator}\n"
        self.indent_level += 1

    def visit_unary_operation(self, unary_operation: UnaryOperation) -> None:
        self.indent_level -= 1

    def pre_visit_binary_operation(self, binary_operation: BinaryOperation) -> None:
        self.output_ast += f"{self.indent()}BinOp: {binary_operation.operator}\n"
        self.indent_level += 1

    def visit_binary_operation(self, binary_operation: BinaryOperation) -> None:
        self.indent_level -= 1

    def pre_visit_new_expression(self, new_expression: NewExpression) -> None:
        self.output_ast += f"{self.indent()}NewExpression\n"
        self.indent_level += 1

    def visit_new_expression(self, new_expression: NewExpression) -> None:
        self.indent_level -= 1

    def pre_visit_data_member_access(
        self, data_member_access: DataMemberAccess
    ) -> None:
        self.output_ast += f"{self.indent()}DataMemberAccess: .\n"
        self.indent_level += 1

    def visit_data_member_access(self, data_member_access: DataMemberAccess) -> None:
        self.indent_level -= 1

    def pre_visit_index_access(self, index_access: IndexAccess) -> None:
        self.output_ast += f"{self.indent()}IndexAccess\n"
        self.indent_level += 1

    def visit_index_access(self, index_access: IndexAccess) -> None:
        self.indent_level -= 1

    def pre_visit_function_call(self, function_call: FunctionCall) -> None:
        self.output_ast += f"{self.indent()}FunctionCall\n"
        self.indent_level += 1

    def visit_function_call(self, function_call: FunctionCall) -> None:
        self.indent_level -= 1

    def pre_visit_case(self, case: Case) -> None:
        self.output_ast += f"{self.indent()}Case\n"
        self.indent_level += 1

    def visit_case(self, case: Case) -> None:
        self.indent_level -= 1

    def pre_visit_case_block(self, case_block: CaseBlock) -> None:
        self.output_ast += f"{self.indent()}CaseBlock\n"
        self.indent_level += 1

    def visit_case_block(self, case_block: CaseBlock) -> None:
        self.indent_level -= 1

    def pre_visit_read_statement(self, read_statement: ReadStatement) -> None:
        self.output_ast += f"{self.indent()}ReadStatement\n"
        self.indent_level += 1

    def visit_read_statement(self, read_statement: ReadStatement) -> None:
        self.indent_level -= 1

    def pre_visit_print_statement(self, print_statement: PrintStatement) -> None:
        self.output_ast += f"{self.indent()}PrintStatement\n"
        self.indent_level += 1

    def visit_print_statement(self, print_statement: PrintStatement) -> None:
        self.indent_level -= 1

    def pre_visit_if_statement(self, if_statement: IfStatement) -> None:
        self.output_ast += f"{self.indent()}IfStatement\n"
        self.indent_level += 1

    def visit_if_statement(self, if_statement: IfStatement) -> None:
        self.indent_level -= 1

    def pre_visit_while_statement(self, while_statement: WhileStatement) -> None:
        self.output_ast += f"{self.indent()}WhileStatement\n"
        self.indent_level += 1

    def visit_while_statement(self, while_statement: WhileStatement) -> None:
        self.indent_level -= 1

    def pre_visit_for_statement(self, for_statement: ForStatement) -> None:
        self.output_ast += f"{self.indent()}ForStatement\n"
        self.indent_level += 1

    def visit_for_statement(self, for_statement: ForStatement) -> None:
        self.indent_level -= 1

    def pre_visit_return_statement(self, return_statement: ReturnStatement) -> None:
        self.output_ast += f"{self.indent()}ReturnStatement\n"
        self.indent_level += 1

    def visit_return_statement(self, return_statement: ReturnStatement) -> None:
        self.indent_level -= 1

    def pre_visit_switch_statement(self, switch_statement: SwitchStatement) -> None:
        self.output_ast += f"{self.indent()}SwitchStatement\n"
        self.indent_level += 1

    def visit_switch_statement(self, switch_statement: SwitchStatement) -> None:
        self.indent_level -= 1

    def pre_visit_block(self, block: Block) -> None:
        self.output_ast += f"{self.indent()}Block\n"
        self.indent_level += 1

    def visit_block(self, block: Block) -> None:
        self.indent_level -= 1

    def pre_visit_class_member(self, class_member: ClassMember) -> None:
        self.output_ast += f"{self.indent()}ClassMember\n"
        self.indent_level += 1

    def visit_class_member(self, class_member: ClassMember) -> None:
        self.indent_level -= 1

    def pre_visit_constructor(self, constructor: Constructor) -> None:
        self.output_ast += f"{self.indent()}Constructor\n"
        self.indent_level += 1

    def visit_constructor(self, constructor: Constructor) -> None:
        self.indent_level -= 1

    def pre_visit_method(self, method: Method) -> None:
        self.output_ast += f"{self.indent()}Method\n"
        self.indent_level += 1

    def visit_method(self, method: Method) -> None:
        self.indent_level -= 1

    def pre_visit_data_member(self, data_member: DataMember) -> None:
        self.output_ast += f"{self.indent()}DataMember\n"
        self.indent_level += 1

    def visit_data_member(self, data_member: DataMember) -> None:
        self.indent_level -= 1

    def pre_visit_class_declaration(self, class_declaration: ClassDeclaration) -> None:
        self.output_ast += f"{self.indent()}Class\n"
        self.indent_level += 1

    def visit_class_declaration(self, class_declaration: ClassDeclaration) -> None:
        self.indent_level -= 1

    def pre_visit_compilation_unit(self, compilation_unit: CompilationUnit) -> None:
        self.output_ast += f"{self.indent()}CompilationUnit\n"
        self.indent_level += 1

    def visit_compilation_unit(self, compilation_unit: CompilationUnit) -> None:
        self.indent_level -= 1

    def __str__(self) -> str:
        return self.output_ast
