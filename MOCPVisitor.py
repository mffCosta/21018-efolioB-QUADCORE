# Generated from MOCP.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MOCPParser import MOCPParser
else:
    from MOCPParser import MOCPParser

# This class defines a complete generic visitor for a parse tree produced by MOCPParser.

class MOCPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MOCPParser#program.
    def visitProgram(self, ctx:MOCPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#prototype.
    def visitPrototype(self, ctx:MOCPParser.PrototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#globalDecl.
    def visitGlobalDecl(self, ctx:MOCPParser.GlobalDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#functionDef.
    def visitFunctionDef(self, ctx:MOCPParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#functionName.
    def visitFunctionName(self, ctx:MOCPParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#paramList.
    def visitParamList(self, ctx:MOCPParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#param.
    def visitParam(self, ctx:MOCPParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#arraySuffix.
    def visitArraySuffix(self, ctx:MOCPParser.ArraySuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#block.
    def visitBlock(self, ctx:MOCPParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#varDecl.
    def visitVarDecl(self, ctx:MOCPParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarSimpleDecl.
    def visitVarSimpleDecl(self, ctx:MOCPParser.VarSimpleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarInitDecl.
    def visitVarInitDecl(self, ctx:MOCPParser.VarInitDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarSizedArrayDecl.
    def visitVarSizedArrayDecl(self, ctx:MOCPParser.VarSizedArrayDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarArrayInitDecl.
    def visitVarArrayInitDecl(self, ctx:MOCPParser.VarArrayInitDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarArrayExprInitDecl.
    def visitVarArrayExprInitDecl(self, ctx:MOCPParser.VarArrayExprInitDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#VarUnsizedArrayDecl.
    def visitVarUnsizedArrayDecl(self, ctx:MOCPParser.VarUnsizedArrayDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#arrayInit.
    def visitArrayInit(self, ctx:MOCPParser.ArrayInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#stmt.
    def visitStmt(self, ctx:MOCPParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#assignStmt.
    def visitAssignStmt(self, ctx:MOCPParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#ifStmt.
    def visitIfStmt(self, ctx:MOCPParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#whileStmt.
    def visitWhileStmt(self, ctx:MOCPParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#forStmt.
    def visitForStmt(self, ctx:MOCPParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#forInit.
    def visitForInit(self, ctx:MOCPParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#forCond.
    def visitForCond(self, ctx:MOCPParser.ForCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#forUpdate.
    def visitForUpdate(self, ctx:MOCPParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#returnStmt.
    def visitReturnStmt(self, ctx:MOCPParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#callStmt.
    def visitCallStmt(self, ctx:MOCPParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#writeStmt.
    def visitWriteStmt(self, ctx:MOCPParser.WriteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#condExpr.
    def visitCondExpr(self, ctx:MOCPParser.CondExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:MOCPParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:MOCPParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#logicalNotExpr.
    def visitLogicalNotExpr(self, ctx:MOCPParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#relationalExpr.
    def visitRelationalExpr(self, ctx:MOCPParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#relOp.
    def visitRelOp(self, ctx:MOCPParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#expr.
    def visitExpr(self, ctx:MOCPParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:MOCPParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:MOCPParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#unaryExpr.
    def visitUnaryExpr(self, ctx:MOCPParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#castExpr.
    def visitCastExpr(self, ctx:MOCPParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:MOCPParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#location.
    def visitLocation(self, ctx:MOCPParser.LocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#inputCall.
    def visitInputCall(self, ctx:MOCPParser.InputCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#userFunctionCall.
    def visitUserFunctionCall(self, ctx:MOCPParser.UserFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#argList.
    def visitArgList(self, ctx:MOCPParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#literal.
    def visitLiteral(self, ctx:MOCPParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#returnType.
    def visitReturnType(self, ctx:MOCPParser.ReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#varType.
    def visitVarType(self, ctx:MOCPParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCPParser#castType.
    def visitCastType(self, ctx:MOCPParser.CastTypeContext):
        return self.visitChildren(ctx)



del MOCPParser