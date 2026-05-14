// Generated from c:/Users/mffcf/MEOCloud/LEI/3 Ano/2Semestre/21018 Compilação/efolio B/efolioB_QUADCORE/MOCP.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link MOCPParser}.
 */
public interface MOCPListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link MOCPParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(MOCPParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(MOCPParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#prototype}.
	 * @param ctx the parse tree
	 */
	void enterPrototype(MOCPParser.PrototypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#prototype}.
	 * @param ctx the parse tree
	 */
	void exitPrototype(MOCPParser.PrototypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#globalDecl}.
	 * @param ctx the parse tree
	 */
	void enterGlobalDecl(MOCPParser.GlobalDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#globalDecl}.
	 * @param ctx the parse tree
	 */
	void exitGlobalDecl(MOCPParser.GlobalDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void enterFunctionDef(MOCPParser.FunctionDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void exitFunctionDef(MOCPParser.FunctionDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#functionName}.
	 * @param ctx the parse tree
	 */
	void enterFunctionName(MOCPParser.FunctionNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#functionName}.
	 * @param ctx the parse tree
	 */
	void exitFunctionName(MOCPParser.FunctionNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#paramList}.
	 * @param ctx the parse tree
	 */
	void enterParamList(MOCPParser.ParamListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#paramList}.
	 * @param ctx the parse tree
	 */
	void exitParamList(MOCPParser.ParamListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#param}.
	 * @param ctx the parse tree
	 */
	void enterParam(MOCPParser.ParamContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#param}.
	 * @param ctx the parse tree
	 */
	void exitParam(MOCPParser.ParamContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#arraySuffix}.
	 * @param ctx the parse tree
	 */
	void enterArraySuffix(MOCPParser.ArraySuffixContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#arraySuffix}.
	 * @param ctx the parse tree
	 */
	void exitArraySuffix(MOCPParser.ArraySuffixContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(MOCPParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(MOCPParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void enterVarDecl(MOCPParser.VarDeclContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#varDecl}.
	 * @param ctx the parse tree
	 */
	void exitVarDecl(MOCPParser.VarDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarSimpleDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarSimpleDecl(MOCPParser.VarSimpleDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarSimpleDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarSimpleDecl(MOCPParser.VarSimpleDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarInitDecl(MOCPParser.VarInitDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarInitDecl(MOCPParser.VarInitDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarSizedArrayDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarSizedArrayDecl(MOCPParser.VarSizedArrayDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarSizedArrayDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarSizedArrayDecl(MOCPParser.VarSizedArrayDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarArrayInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarArrayInitDecl(MOCPParser.VarArrayInitDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarArrayInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarArrayInitDecl(MOCPParser.VarArrayInitDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarArrayExprInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarArrayExprInitDecl(MOCPParser.VarArrayExprInitDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarArrayExprInitDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarArrayExprInitDecl(MOCPParser.VarArrayExprInitDeclContext ctx);
	/**
	 * Enter a parse tree produced by the {@code VarUnsizedArrayDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void enterVarUnsizedArrayDecl(MOCPParser.VarUnsizedArrayDeclContext ctx);
	/**
	 * Exit a parse tree produced by the {@code VarUnsizedArrayDecl}
	 * labeled alternative in {@link MOCPParser#varItem}.
	 * @param ctx the parse tree
	 */
	void exitVarUnsizedArrayDecl(MOCPParser.VarUnsizedArrayDeclContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#arrayInit}.
	 * @param ctx the parse tree
	 */
	void enterArrayInit(MOCPParser.ArrayInitContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#arrayInit}.
	 * @param ctx the parse tree
	 */
	void exitArrayInit(MOCPParser.ArrayInitContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(MOCPParser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(MOCPParser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void enterAssignStmt(MOCPParser.AssignStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#assignStmt}.
	 * @param ctx the parse tree
	 */
	void exitAssignStmt(MOCPParser.AssignStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(MOCPParser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(MOCPParser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void enterWhileStmt(MOCPParser.WhileStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#whileStmt}.
	 * @param ctx the parse tree
	 */
	void exitWhileStmt(MOCPParser.WhileStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#forStmt}.
	 * @param ctx the parse tree
	 */
	void enterForStmt(MOCPParser.ForStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#forStmt}.
	 * @param ctx the parse tree
	 */
	void exitForStmt(MOCPParser.ForStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#forInit}.
	 * @param ctx the parse tree
	 */
	void enterForInit(MOCPParser.ForInitContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#forInit}.
	 * @param ctx the parse tree
	 */
	void exitForInit(MOCPParser.ForInitContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#forCond}.
	 * @param ctx the parse tree
	 */
	void enterForCond(MOCPParser.ForCondContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#forCond}.
	 * @param ctx the parse tree
	 */
	void exitForCond(MOCPParser.ForCondContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#forUpdate}.
	 * @param ctx the parse tree
	 */
	void enterForUpdate(MOCPParser.ForUpdateContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#forUpdate}.
	 * @param ctx the parse tree
	 */
	void exitForUpdate(MOCPParser.ForUpdateContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void enterReturnStmt(MOCPParser.ReturnStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#returnStmt}.
	 * @param ctx the parse tree
	 */
	void exitReturnStmt(MOCPParser.ReturnStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#callStmt}.
	 * @param ctx the parse tree
	 */
	void enterCallStmt(MOCPParser.CallStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#callStmt}.
	 * @param ctx the parse tree
	 */
	void exitCallStmt(MOCPParser.CallStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#writeStmt}.
	 * @param ctx the parse tree
	 */
	void enterWriteStmt(MOCPParser.WriteStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#writeStmt}.
	 * @param ctx the parse tree
	 */
	void exitWriteStmt(MOCPParser.WriteStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#condExpr}.
	 * @param ctx the parse tree
	 */
	void enterCondExpr(MOCPParser.CondExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#condExpr}.
	 * @param ctx the parse tree
	 */
	void exitCondExpr(MOCPParser.CondExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#logicalOrExpr}.
	 * @param ctx the parse tree
	 */
	void enterLogicalOrExpr(MOCPParser.LogicalOrExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#logicalOrExpr}.
	 * @param ctx the parse tree
	 */
	void exitLogicalOrExpr(MOCPParser.LogicalOrExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#logicalAndExpr}.
	 * @param ctx the parse tree
	 */
	void enterLogicalAndExpr(MOCPParser.LogicalAndExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#logicalAndExpr}.
	 * @param ctx the parse tree
	 */
	void exitLogicalAndExpr(MOCPParser.LogicalAndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#logicalNotExpr}.
	 * @param ctx the parse tree
	 */
	void enterLogicalNotExpr(MOCPParser.LogicalNotExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#logicalNotExpr}.
	 * @param ctx the parse tree
	 */
	void exitLogicalNotExpr(MOCPParser.LogicalNotExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelationalExpr(MOCPParser.RelationalExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#relationalExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelationalExpr(MOCPParser.RelationalExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#relOp}.
	 * @param ctx the parse tree
	 */
	void enterRelOp(MOCPParser.RelOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#relOp}.
	 * @param ctx the parse tree
	 */
	void exitRelOp(MOCPParser.RelOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(MOCPParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(MOCPParser.ExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#additiveExpr}.
	 * @param ctx the parse tree
	 */
	void enterAdditiveExpr(MOCPParser.AdditiveExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#additiveExpr}.
	 * @param ctx the parse tree
	 */
	void exitAdditiveExpr(MOCPParser.AdditiveExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#multiplicativeExpr}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicativeExpr(MOCPParser.MultiplicativeExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#multiplicativeExpr}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicativeExpr(MOCPParser.MultiplicativeExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryExpr(MOCPParser.UnaryExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryExpr(MOCPParser.UnaryExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void enterCastExpr(MOCPParser.CastExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void exitCastExpr(MOCPParser.CastExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#primaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterPrimaryExpr(MOCPParser.PrimaryExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#primaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitPrimaryExpr(MOCPParser.PrimaryExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#location}.
	 * @param ctx the parse tree
	 */
	void enterLocation(MOCPParser.LocationContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#location}.
	 * @param ctx the parse tree
	 */
	void exitLocation(MOCPParser.LocationContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#inputCall}.
	 * @param ctx the parse tree
	 */
	void enterInputCall(MOCPParser.InputCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#inputCall}.
	 * @param ctx the parse tree
	 */
	void exitInputCall(MOCPParser.InputCallContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#userFunctionCall}.
	 * @param ctx the parse tree
	 */
	void enterUserFunctionCall(MOCPParser.UserFunctionCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#userFunctionCall}.
	 * @param ctx the parse tree
	 */
	void exitUserFunctionCall(MOCPParser.UserFunctionCallContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#argList}.
	 * @param ctx the parse tree
	 */
	void enterArgList(MOCPParser.ArgListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#argList}.
	 * @param ctx the parse tree
	 */
	void exitArgList(MOCPParser.ArgListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(MOCPParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(MOCPParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#returnType}.
	 * @param ctx the parse tree
	 */
	void enterReturnType(MOCPParser.ReturnTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#returnType}.
	 * @param ctx the parse tree
	 */
	void exitReturnType(MOCPParser.ReturnTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#varType}.
	 * @param ctx the parse tree
	 */
	void enterVarType(MOCPParser.VarTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#varType}.
	 * @param ctx the parse tree
	 */
	void exitVarType(MOCPParser.VarTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCPParser#castType}.
	 * @param ctx the parse tree
	 */
	void enterCastType(MOCPParser.CastTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCPParser#castType}.
	 * @param ctx the parse tree
	 */
	void exitCastType(MOCPParser.CastTypeContext ctx);
}