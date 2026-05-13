# Generated from MOCP.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MOCPParser import MOCPParser
else:
    from MOCPParser import MOCPParser

# This class defines a complete listener for a parse tree produced by MOCPParser.
class MOCPListener(ParseTreeListener):

    # Enter a parse tree produced by MOCPParser#program.
    def enterProgram(self, ctx:MOCPParser.ProgramContext):
        pass

    # Exit a parse tree produced by MOCPParser#program.
    def exitProgram(self, ctx:MOCPParser.ProgramContext):
        pass


    # Enter a parse tree produced by MOCPParser#prototype.
    def enterPrototype(self, ctx:MOCPParser.PrototypeContext):
        pass

    # Exit a parse tree produced by MOCPParser#prototype.
    def exitPrototype(self, ctx:MOCPParser.PrototypeContext):
        pass


    # Enter a parse tree produced by MOCPParser#globalDecl.
    def enterGlobalDecl(self, ctx:MOCPParser.GlobalDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#globalDecl.
    def exitGlobalDecl(self, ctx:MOCPParser.GlobalDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#functionDef.
    def enterFunctionDef(self, ctx:MOCPParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by MOCPParser#functionDef.
    def exitFunctionDef(self, ctx:MOCPParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by MOCPParser#functionName.
    def enterFunctionName(self, ctx:MOCPParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by MOCPParser#functionName.
    def exitFunctionName(self, ctx:MOCPParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by MOCPParser#paramList.
    def enterParamList(self, ctx:MOCPParser.ParamListContext):
        pass

    # Exit a parse tree produced by MOCPParser#paramList.
    def exitParamList(self, ctx:MOCPParser.ParamListContext):
        pass


    # Enter a parse tree produced by MOCPParser#param.
    def enterParam(self, ctx:MOCPParser.ParamContext):
        pass

    # Exit a parse tree produced by MOCPParser#param.
    def exitParam(self, ctx:MOCPParser.ParamContext):
        pass


    # Enter a parse tree produced by MOCPParser#arraySuffix.
    def enterArraySuffix(self, ctx:MOCPParser.ArraySuffixContext):
        pass

    # Exit a parse tree produced by MOCPParser#arraySuffix.
    def exitArraySuffix(self, ctx:MOCPParser.ArraySuffixContext):
        pass


    # Enter a parse tree produced by MOCPParser#block.
    def enterBlock(self, ctx:MOCPParser.BlockContext):
        pass

    # Exit a parse tree produced by MOCPParser#block.
    def exitBlock(self, ctx:MOCPParser.BlockContext):
        pass


    # Enter a parse tree produced by MOCPParser#varDecl.
    def enterVarDecl(self, ctx:MOCPParser.VarDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#varDecl.
    def exitVarDecl(self, ctx:MOCPParser.VarDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarSimpleDecl.
    def enterVarSimpleDecl(self, ctx:MOCPParser.VarSimpleDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarSimpleDecl.
    def exitVarSimpleDecl(self, ctx:MOCPParser.VarSimpleDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarInitDecl.
    def enterVarInitDecl(self, ctx:MOCPParser.VarInitDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarInitDecl.
    def exitVarInitDecl(self, ctx:MOCPParser.VarInitDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarSizedArrayDecl.
    def enterVarSizedArrayDecl(self, ctx:MOCPParser.VarSizedArrayDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarSizedArrayDecl.
    def exitVarSizedArrayDecl(self, ctx:MOCPParser.VarSizedArrayDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarArrayInitDecl.
    def enterVarArrayInitDecl(self, ctx:MOCPParser.VarArrayInitDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarArrayInitDecl.
    def exitVarArrayInitDecl(self, ctx:MOCPParser.VarArrayInitDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarArrayExprInitDecl.
    def enterVarArrayExprInitDecl(self, ctx:MOCPParser.VarArrayExprInitDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarArrayExprInitDecl.
    def exitVarArrayExprInitDecl(self, ctx:MOCPParser.VarArrayExprInitDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#VarUnsizedArrayDecl.
    def enterVarUnsizedArrayDecl(self, ctx:MOCPParser.VarUnsizedArrayDeclContext):
        pass

    # Exit a parse tree produced by MOCPParser#VarUnsizedArrayDecl.
    def exitVarUnsizedArrayDecl(self, ctx:MOCPParser.VarUnsizedArrayDeclContext):
        pass


    # Enter a parse tree produced by MOCPParser#arrayInit.
    def enterArrayInit(self, ctx:MOCPParser.ArrayInitContext):
        pass

    # Exit a parse tree produced by MOCPParser#arrayInit.
    def exitArrayInit(self, ctx:MOCPParser.ArrayInitContext):
        pass


    # Enter a parse tree produced by MOCPParser#stmt.
    def enterStmt(self, ctx:MOCPParser.StmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#stmt.
    def exitStmt(self, ctx:MOCPParser.StmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#assignStmt.
    def enterAssignStmt(self, ctx:MOCPParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#assignStmt.
    def exitAssignStmt(self, ctx:MOCPParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#ifStmt.
    def enterIfStmt(self, ctx:MOCPParser.IfStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#ifStmt.
    def exitIfStmt(self, ctx:MOCPParser.IfStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#whileStmt.
    def enterWhileStmt(self, ctx:MOCPParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#whileStmt.
    def exitWhileStmt(self, ctx:MOCPParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#forStmt.
    def enterForStmt(self, ctx:MOCPParser.ForStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#forStmt.
    def exitForStmt(self, ctx:MOCPParser.ForStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#forInit.
    def enterForInit(self, ctx:MOCPParser.ForInitContext):
        pass

    # Exit a parse tree produced by MOCPParser#forInit.
    def exitForInit(self, ctx:MOCPParser.ForInitContext):
        pass


    # Enter a parse tree produced by MOCPParser#forCond.
    def enterForCond(self, ctx:MOCPParser.ForCondContext):
        pass

    # Exit a parse tree produced by MOCPParser#forCond.
    def exitForCond(self, ctx:MOCPParser.ForCondContext):
        pass


    # Enter a parse tree produced by MOCPParser#forUpdate.
    def enterForUpdate(self, ctx:MOCPParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by MOCPParser#forUpdate.
    def exitForUpdate(self, ctx:MOCPParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by MOCPParser#returnStmt.
    def enterReturnStmt(self, ctx:MOCPParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#returnStmt.
    def exitReturnStmt(self, ctx:MOCPParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#callStmt.
    def enterCallStmt(self, ctx:MOCPParser.CallStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#callStmt.
    def exitCallStmt(self, ctx:MOCPParser.CallStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#writeStmt.
    def enterWriteStmt(self, ctx:MOCPParser.WriteStmtContext):
        pass

    # Exit a parse tree produced by MOCPParser#writeStmt.
    def exitWriteStmt(self, ctx:MOCPParser.WriteStmtContext):
        pass


    # Enter a parse tree produced by MOCPParser#condExpr.
    def enterCondExpr(self, ctx:MOCPParser.CondExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#condExpr.
    def exitCondExpr(self, ctx:MOCPParser.CondExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:MOCPParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:MOCPParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:MOCPParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:MOCPParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#logicalNotExpr.
    def enterLogicalNotExpr(self, ctx:MOCPParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#logicalNotExpr.
    def exitLogicalNotExpr(self, ctx:MOCPParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#relationalExpr.
    def enterRelationalExpr(self, ctx:MOCPParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#relationalExpr.
    def exitRelationalExpr(self, ctx:MOCPParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#relOp.
    def enterRelOp(self, ctx:MOCPParser.RelOpContext):
        pass

    # Exit a parse tree produced by MOCPParser#relOp.
    def exitRelOp(self, ctx:MOCPParser.RelOpContext):
        pass


    # Enter a parse tree produced by MOCPParser#expr.
    def enterExpr(self, ctx:MOCPParser.ExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#expr.
    def exitExpr(self, ctx:MOCPParser.ExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:MOCPParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:MOCPParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:MOCPParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:MOCPParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#unaryExpr.
    def enterUnaryExpr(self, ctx:MOCPParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#unaryExpr.
    def exitUnaryExpr(self, ctx:MOCPParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#castExpr.
    def enterCastExpr(self, ctx:MOCPParser.CastExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#castExpr.
    def exitCastExpr(self, ctx:MOCPParser.CastExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:MOCPParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by MOCPParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:MOCPParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by MOCPParser#location.
    def enterLocation(self, ctx:MOCPParser.LocationContext):
        pass

    # Exit a parse tree produced by MOCPParser#location.
    def exitLocation(self, ctx:MOCPParser.LocationContext):
        pass


    # Enter a parse tree produced by MOCPParser#inputCall.
    def enterInputCall(self, ctx:MOCPParser.InputCallContext):
        pass

    # Exit a parse tree produced by MOCPParser#inputCall.
    def exitInputCall(self, ctx:MOCPParser.InputCallContext):
        pass


    # Enter a parse tree produced by MOCPParser#userFunctionCall.
    def enterUserFunctionCall(self, ctx:MOCPParser.UserFunctionCallContext):
        pass

    # Exit a parse tree produced by MOCPParser#userFunctionCall.
    def exitUserFunctionCall(self, ctx:MOCPParser.UserFunctionCallContext):
        pass


    # Enter a parse tree produced by MOCPParser#argList.
    def enterArgList(self, ctx:MOCPParser.ArgListContext):
        pass

    # Exit a parse tree produced by MOCPParser#argList.
    def exitArgList(self, ctx:MOCPParser.ArgListContext):
        pass


    # Enter a parse tree produced by MOCPParser#literal.
    def enterLiteral(self, ctx:MOCPParser.LiteralContext):
        pass

    # Exit a parse tree produced by MOCPParser#literal.
    def exitLiteral(self, ctx:MOCPParser.LiteralContext):
        pass


    # Enter a parse tree produced by MOCPParser#returnType.
    def enterReturnType(self, ctx:MOCPParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by MOCPParser#returnType.
    def exitReturnType(self, ctx:MOCPParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by MOCPParser#varType.
    def enterVarType(self, ctx:MOCPParser.VarTypeContext):
        pass

    # Exit a parse tree produced by MOCPParser#varType.
    def exitVarType(self, ctx:MOCPParser.VarTypeContext):
        pass


    # Enter a parse tree produced by MOCPParser#castType.
    def enterCastType(self, ctx:MOCPParser.CastTypeContext):
        pass

    # Exit a parse tree produced by MOCPParser#castType.
    def exitCastType(self, ctx:MOCPParser.CastTypeContext):
        pass



del MOCPParser