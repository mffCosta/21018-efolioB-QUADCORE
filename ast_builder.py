"""
ast_builder.py — Construção da Árvore de Sintaxe Abstrata (AST) a partir da parse tree ANTLR.
UC 21018 — Compilação, Universidade Aberta, 2025/2026
Autores: Maria Costa (2304361) | João Rodrigues (2203474) | Nuno Rolo (1900405) | Flávio Oliveira (1900860)
Grupo: QUADCORE
"""

from MOCPVisitor import MOCPVisitor
from MOCPParser import MOCPParser

from ast_nodes import (
    ProgramNode,
    PrototypeNode,
    FunctionDefNode,
    ParamNode,
    BlockNode,
    VarDeclNode,
    VarSimpleDeclNode,
    VarInitDeclNode,
    VarSizedArrayDeclNode,
    VarUnsizedArrayDeclNode,
    VarArrayInitDeclNode,
    VarArrayExprInitDeclNode,
    AssignStmtNode,
    IfStmtNode,
    WhileStmtNode,
    ForStmtNode,
    ReturnStmtNode,
    ExprStmtNode,
    EmptyStmtNode,
    AssignExprNode,
    RelationalCondNode,
    NotCondNode,
    BinaryLogicalCondNode,
    ExprAsCondNode,
    BinaryExprNode,
    UnaryExprNode,
    CastExprNode,
    IdentifierNode,
    ArrayAccessNode,
    FunctionCallNode,
    IntLiteralNode,
    RealLiteralNode,
    StringLiteralNode,
)


class ASTBuilderVisitor(MOCPVisitor):
    """
    Constrói uma AST abstrata a partir da parse tree gerada pelo ANTLR.
    Implementação compatível com a gramática final MOCP.g4.
    """

    # =====================================================
    # Helpers
    # =====================================================

    def _strip_quotes(self, text: str) -> str:
        if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
            return text[1:-1]
        return text

    def _build_left_associative_binary_expr(self, nodes, ctx):
        """
        Constrói uma árvore binária associativa à esquerda a partir de:
            a op b op c op d
        """
        result = nodes[0]
        idx = 1

        for child_pos in range(1, ctx.getChildCount(), 2):
            op = ctx.getChild(child_pos).getText()
            result = BinaryExprNode(
                left=result,
                operator=op,
                right=nodes[idx]
            )
            idx += 1

        return result

    # =====================================================
    # Programa
    # =====================================================

    def visitProgram(self, ctx: MOCPParser.ProgramContext):
        return ProgramNode(
            prototypes=[self.visit(p) for p in ctx.prototype()],
            global_decls=[self.visit(g) for g in ctx.globalDecl()],
            functions=[self.visit(f) for f in ctx.functionDef()],
        )

    # =====================================================
    # Protótipos / Funções
    # =====================================================

    def visitPrototype(self, ctx: MOCPParser.PrototypeContext):
        params = self.visit(ctx.paramList()) if ctx.paramList() else []

        return PrototypeNode(
            return_type=ctx.returnType().getText(),
            name=ctx.functionName().getText(),
            params=params,
        )

    def visitGlobalDecl(self, ctx: MOCPParser.GlobalDeclContext):
        return self.visit(ctx.varDecl())

    def visitFunctionDef(self, ctx: MOCPParser.FunctionDefContext):
        params = self.visit(ctx.paramList()) if ctx.paramList() else []

        return FunctionDefNode(
            return_type=ctx.returnType().getText(),
            name=ctx.functionName().getText(),
            params=params,
            body=self.visit(ctx.block()),
        )

    def visitFunctionName(self, ctx: MOCPParser.FunctionNameContext):
        return ctx.getText()

    # =====================================================
    # Parâmetros
    # =====================================================

    def visitParamList(self, ctx: MOCPParser.ParamListContext):
        if ctx.VAZIO():
            return []
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: MOCPParser.ParamContext):
        name = ctx.ID().getText() if ctx.ID() else ""
        is_array = ctx.arraySuffix() is not None

        return ParamNode(
            param_type=ctx.varType().getText(),
            name=name,
            is_array=is_array,
        )

    def visitArraySuffix(self, ctx: MOCPParser.ArraySuffixContext):
        return "[]"

    # =====================================================
    # Blocos / Declarações
    # =====================================================

    def visitBlock(self, ctx: MOCPParser.BlockContext):
        return BlockNode(
            declarations=[self.visit(d) for d in ctx.varDecl()],
            statements=[self.visit(s) for s in ctx.stmt()],
        )

    def visitVarDecl(self, ctx: MOCPParser.VarDeclContext):
        return VarDeclNode(
            var_type=ctx.varType().getText(),
            items=[self.visit(item) for item in ctx.varItem()],
        )

    # -----------------------------------------------------
    # varItem labelled alternatives
    # -----------------------------------------------------

    def visitVarSimpleDecl(self, ctx: MOCPParser.VarSimpleDeclContext):
        return VarSimpleDeclNode(
            name=ctx.ID().getText()
        )

    def visitVarInitDecl(self, ctx: MOCPParser.VarInitDeclContext):
        return VarInitDeclNode(
            name=ctx.ID().getText(),
            value=self.visit(ctx.expr())
        )

    def visitVarSizedArrayDecl(self, ctx: MOCPParser.VarSizedArrayDeclContext):
        return VarSizedArrayDeclNode(
            name=ctx.ID().getText(),
            size=int(ctx.INT_LITERAL().getText())
        )

    def visitVarArrayInitDecl(self, ctx: MOCPParser.VarArrayInitDeclContext):
        return VarArrayInitDeclNode(
            name=ctx.ID().getText(),
            values=self.visit(ctx.arrayInit())
        )

    def visitVarArrayExprInitDecl(self, ctx: MOCPParser.VarArrayExprInitDeclContext):
        return VarArrayExprInitDeclNode(
            name=ctx.ID().getText(),
            value=self.visit(ctx.expr())
        )

    def visitVarUnsizedArrayDecl(self, ctx: MOCPParser.VarUnsizedArrayDeclContext):
        return VarUnsizedArrayDeclNode(
            name=ctx.ID().getText()
        )

    def visitArrayInit(self, ctx: MOCPParser.ArrayInitContext):
        return [self.visit(e) for e in ctx.expr()]

    # =====================================================
    # Instruções
    # =====================================================

    def visitStmt(self, ctx: MOCPParser.StmtContext):
        if ctx.assignStmt():
            return self.visit(ctx.assignStmt())
        if ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        if ctx.whileStmt():
            return self.visit(ctx.whileStmt())
        if ctx.forStmt():
            return self.visit(ctx.forStmt())
        if ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        if ctx.writeStmt():
            return self.visit(ctx.writeStmt())
        if ctx.callStmt():
            return self.visit(ctx.callStmt())
        if ctx.block():
            return self.visit(ctx.block())
        return EmptyStmtNode()

    def visitAssignStmt(self, ctx: MOCPParser.AssignStmtContext):
        return AssignStmtNode(
            target=self.visit(ctx.location()),
            value=self.visit(ctx.expr())
        )

    def visitIfStmt(self, ctx: MOCPParser.IfStmtContext):
        blocks = ctx.block()

        then_block = self.visit(blocks[0])
        else_block = self.visit(blocks[1]) if len(blocks) > 1 else None

        return IfStmtNode(
            condition=self.visit(ctx.condExpr()),
            then_block=then_block,
            else_block=else_block
        )

    def visitWhileStmt(self, ctx: MOCPParser.WhileStmtContext):
        return WhileStmtNode(
            condition=self.visit(ctx.condExpr()),
            body=self.visit(ctx.block())
        )

    def visitForStmt(self, ctx: MOCPParser.ForStmtContext):
        return ForStmtNode(
            init=self.visit(ctx.forInit()) if ctx.forInit() else None,
            condition=self.visit(ctx.forCond()) if ctx.forCond() else None,
            update=self.visit(ctx.forUpdate()) if ctx.forUpdate() else None,
            body=self.visit(ctx.block())
        )

    def visitForInit(self, ctx: MOCPParser.ForInitContext):
        return AssignExprNode(
            target=self.visit(ctx.location()),
            value=self.visit(ctx.expr())
        )

    def visitForCond(self, ctx: MOCPParser.ForCondContext):
        return self.visit(ctx.condExpr())

    def visitForUpdate(self, ctx: MOCPParser.ForUpdateContext):
        return AssignExprNode(
            target=self.visit(ctx.location()),
            value=self.visit(ctx.expr())
        )

    def visitReturnStmt(self, ctx: MOCPParser.ReturnStmtContext):
        return ReturnStmtNode(
            value=self.visit(ctx.expr()) if ctx.expr() else None
        )

    def visitCallStmt(self, ctx: MOCPParser.CallStmtContext):
        return ExprStmtNode(
            expr=self.visit(ctx.userFunctionCall())
        )

    def visitWriteStmt(self, ctx: MOCPParser.WriteStmtContext):
        """
        Representa escrita como chamada reservada de função.
        escrever(expr);
        escreverc(expr);
        escrevers(expr);
        escreverv(id);
        """
        if ctx.ESCREVER():
            return ExprStmtNode(
                expr=FunctionCallNode(
                    name="escrever",
                    args=[self.visit(ctx.expr())],
                    is_reserved_io=True
                )
            )

        if ctx.ESCREVERC():
            return ExprStmtNode(
                expr=FunctionCallNode(
                    name="escreverc",
                    args=[self.visit(ctx.expr())],
                    is_reserved_io=True
                )
            )

        if ctx.ESCREVERS():
            return ExprStmtNode(
                expr=FunctionCallNode(
                    name="escrevers",
                    args=[self.visit(ctx.expr())],
                    is_reserved_io=True
                )
            )

        # ESCREVERV(ID)
        return ExprStmtNode(
            expr=FunctionCallNode(
                name="escreverv",
                args=[IdentifierNode(ctx.ID().getText())],
                is_reserved_io=True
            )
        )

    # =====================================================
    # Condições
    # =====================================================

    def visitCondExpr(self, ctx: MOCPParser.CondExprContext):
        return self.visit(ctx.logicalOrExpr())

    def visitLogicalOrExpr(self, ctx: MOCPParser.LogicalOrExprContext):
        nodes = [self.visit(c) for c in ctx.logicalAndExpr()]
        result = nodes[0]

        for i in range(1, len(nodes)):
            result = BinaryLogicalCondNode(
                left=result,
                operator='||',
                right=nodes[i]
            )

        return result

    def visitLogicalAndExpr(self, ctx: MOCPParser.LogicalAndExprContext):
        nodes = [self.visit(c) for c in ctx.logicalNotExpr()]
        result = nodes[0]

        for i in range(1, len(nodes)):
            result = BinaryLogicalCondNode(
                left=result,
                operator='&&',
                right=nodes[i]
            )

        return result

    def visitLogicalNotExpr(self, ctx: MOCPParser.LogicalNotExprContext):
        if ctx.NOT():
            return NotCondNode(
                operand=self.visit(ctx.logicalNotExpr())
            )
        return self.visit(ctx.relationalExpr())

    def visitRelationalExpr(self, ctx: MOCPParser.RelationalExprContext):
        # caso: '(' condExpr ')'
        if ctx.condExpr():
            return self.visit(ctx.condExpr())

        exprs = ctx.expr()

        # caso: condição é só uma expressão
        if len(exprs) == 1:
            return ExprAsCondNode(
                expr=self.visit(exprs[0])
            )

        # caso relacional: expr op expr
        return RelationalCondNode(
            left=self.visit(exprs[0]),
            operator=self.visit(ctx.relOp()),
            right=self.visit(exprs[1])
        )

    def visitRelOp(self, ctx: MOCPParser.RelOpContext):
        return ctx.getText()

    # =====================================================
    # Expressões
    # =====================================================

    def visitExpr(self, ctx: MOCPParser.ExprContext):
        return self.visit(ctx.additiveExpr())

    def visitAdditiveExpr(self, ctx: MOCPParser.AdditiveExprContext):
        nodes = [self.visit(m) for m in ctx.multiplicativeExpr()]
        return self._build_left_associative_binary_expr(nodes, ctx)

    def visitMultiplicativeExpr(self, ctx: MOCPParser.MultiplicativeExprContext):
        nodes = [self.visit(u) for u in ctx.unaryExpr()]
        return self._build_left_associative_binary_expr(nodes, ctx)

    def visitUnaryExpr(self, ctx: MOCPParser.UnaryExprContext):
        if ctx.MINUS():
            return UnaryExprNode(
                operator='-',
                operand=self.visit(ctx.unaryExpr())
            )
        return self.visit(ctx.castExpr())

    def visitCastExpr(self, ctx: MOCPParser.CastExprContext):
        if ctx.castType():
            return CastExprNode(
                target_type=ctx.castType().getText(),
                expr=self.visit(ctx.unaryExpr())
            )
        return self.visit(ctx.primaryExpr())

    def visitPrimaryExpr(self, ctx: MOCPParser.PrimaryExprContext):
        if ctx.location():
            return self.visit(ctx.location())
        if ctx.inputCall():
            return self.visit(ctx.inputCall())
        if ctx.userFunctionCall():
            return self.visit(ctx.userFunctionCall())
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.expr():
            # AST abstrata: não preserva parênteses
            return self.visit(ctx.expr())

        raise ValueError("Expressão primária inválida.")

    # =====================================================
    # Localizações
    # =====================================================

    def visitLocation(self, ctx: MOCPParser.LocationContext):
        if ctx.LBRACK():
            return ArrayAccessNode(
                name=ctx.ID().getText(),
                index=self.visit(ctx.expr())
            )
        return IdentifierNode(
            name=ctx.ID().getText()
        )

    # =====================================================
    # Chamadas
    # =====================================================

    def visitInputCall(self, ctx: MOCPParser.InputCallContext):
        if ctx.LER():
            return FunctionCallNode(
                name="ler",
                args=[],
                is_reserved_io=True
            )
        if ctx.LERC():
            return FunctionCallNode(
                name="lerc",
                args=[],
                is_reserved_io=True
            )
        return FunctionCallNode(
            name="lers",
            args=[],
            is_reserved_io=True
        )

    def visitUserFunctionCall(self, ctx: MOCPParser.UserFunctionCallContext):
        args = self.visit(ctx.argList()) if ctx.argList() else []

        return FunctionCallNode(
            name=ctx.functionName().getText(),
            args=args,
            is_reserved_io=False
        )

    def visitArgList(self, ctx: MOCPParser.ArgListContext):
        return [self.visit(e) for e in ctx.expr()]

    # =====================================================
    # Literais
    # =====================================================

    def visitLiteral(self, ctx: MOCPParser.LiteralContext):
        if ctx.INT_LITERAL():
            return IntLiteralNode(
                value=int(ctx.INT_LITERAL().getText())
            )

        if ctx.REAL_LITERAL():
            return RealLiteralNode(
                value=float(ctx.REAL_LITERAL().getText())
            )

        if ctx.STRING_LITERAL():
            return StringLiteralNode(
                value=self._strip_quotes(ctx.STRING_LITERAL().getText())
            )

        raise ValueError("Literal inválido.")