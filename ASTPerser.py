
import ast



class ASTPerser:

    methods_functions = []

    @staticmethod
    def show_func_name(functionNode):

        print("Function name:", functionNode.name)

    @staticmethod
    def GetListFunc():

        return methods_functions

    @staticmethod
    def show_func_args(functionNode):

        arg_list = ASTPerser.get_func_arg(functionNode)
        for arrg in arg_list:
            print("\tParameter name:", arrg)

    @staticmethod
    def get_func_arg(functionNode):

        func_arg = []
        for argument in functionNode.args.args:
            func_arg += [argument.arg]

        return func_arg

    @staticmethod
    def Get_Function_Node(node):

        return [f for f in node.body if isinstance(f, ast.FunctionDef)]

    @staticmethod
    def Get_Class_Node(node):

        return [f for f in node.body if isinstance(f, ast.ClassDef)]

    @staticmethod
    def Get_Function_In_Class(classes):
        methods = []
        for c in classes:
            methods += [m for m in c.body if isinstance(m, ast.FunctionDef)]
        return methods

    @staticmethod
    def Get_Methods_In_Code(functionNode):
        global methods_functions
        functions = ASTPerser.Get_Function_Node(functionNode)

        classes = ASTPerser.Get_Class_Node(functionNode)
        methods = ASTPerser.Get_Function_In_Class(classes)
        methods_functions = functions + methods

        return methods_functions

    @staticmethod
    def Get_If_Node(functionNode):

        return [m for m in functionNode.body if isinstance(m, ast.If)]

    @staticmethod
    def get_Return(functionNode):

        return [m for m in functionNode.body if isinstance(m, ast.Return)]

    @staticmethod
    def show_returns(functionNode):

        x = ASTPerser.get_Return(functionNode)

        if x:
            return True
        else:
            return False

    @staticmethod
    def Get_returns_Value(functionNode):

        x = ASTPerser.get_Return(functionNode)
        for i in x:

            if isinstance(i.value, ast.Name):
                ReturnValue = i.value.id

        return ReturnValue

    @staticmethod
    def Get_Expr_Node(functionNode):

        return [m for m in functionNode.body if isinstance(m, ast.Expr)]

    @staticmethod
    def Get_Assign_Node(functionNode):

        return [m for m in functionNode.body if isinstance(m, ast.Assign)]

    @staticmethod
    def show_ifstatement(functionNode):
        print("If stat :")
        x = ASTPerser.Get_If_Node(functionNode)
        if x:
            print("\t\t yes ")
        else:
            print("\t\t no ")

    @staticmethod
    def ExistIf(functionNode):
        x = ASTPerser.Get_If_Node(functionNode)
        if x:
            return True
        else:
            return False

    @staticmethod
    def LeftValueIf(functionNode):

        x = ASTPerser.Get_If_Node(functionNode)
        for element in x:
            if isinstance(element.test, ast.Compare):
                Left_value_if = element.test.left.id
        return Left_value_if

    @staticmethod
    def OperandAttValueIf(functionNode):

        ## deux types de if boolop et compare ..

        x = ASTPerser.Get_If_Node(functionNode)
        for element in x:
            if isinstance(element.test, ast.BoolOp):
                for j in element.test.values:
                    if isinstance(j.operand, ast.Attribute):
                        Operand_Att_Value_If = j.operand.value.id
                        return Operand_Att_Value_If
            elif isinstance(element.test, ast.Compare):
                Operand_Att_Value_If = element.test.left.id
                return Operand_Att_Value_If
            else:
                Operand_Att_Value_If = "rien"
                return Operand_Att_Value_If

    @staticmethod
    def AllCalls(functionNode):
        AllFuncCalls = []
        callscases = []

        callscases = ASTPerser.CallsCases(functionNode)
        AllFuncCalls = callscases

        return AllFuncCalls

    @staticmethod
    def RecursiveNode(functionNode):
        CallsIn1 = []
        CallsIn2 = []
        CallsIn = []
        test = False

        for i in functionNode.body:
            test = ASTPerser.CallsInBodies(i)
            if test == True:
                CallsIn1 = ASTPerser.CallsCases(i)
                if (isinstance(i, ast.If) == True):
                    CallsIn2 = ASTPerser.CallsInOrelse(i)

                CallsIn = CallsIn + CallsIn2 + CallsIn1 + ASTPerser.RecursiveNode(i)

        return CallsIn

    @staticmethod
    def CallsInOrelse(Node):
        CallsIn = []
        listcalls = []

        for arg in Node.orelse:
            testt = ASTPerser.CallsInBodies(arg)
            if testt == True:
                None
            else:
                if isinstance(arg, ast.Expr):
                    if isinstance(arg.value, ast.Call):
                        if isinstance(arg.value.func, ast.Attribute):
                            listcalls += [arg.value.func.attr]
                        else:
                            listcalls += [arg.value.func.id]
                elif isinstance(arg, ast.Assign):
                    if isinstance(arg.value, ast.Call):
                        if isinstance(arg.value.func, ast.Attribute):
                            listcalls += [arg.value.func.attr]
                        else:
                            listcalls += [arg.value.func.id]
                elif isinstance(arg, ast.Call):
                    if isinstance(arg.func, ast.Attribute):
                        if isinstance(arg.func.value, ast.Name):
                            listcalls += [arg.func.value.attr]

        return listcalls

    @staticmethod
    def CallsInBodies(Node):
        ValTest = 0
        if (isinstance(Node, ast.If) == True):
            ValTest = 1
        elif (isinstance(Node, ast.With) == True):
            ValTest = 1
        elif (isinstance(Node, ast.While) == True):
            ValTest = 1
        elif (isinstance(Node, ast.For) == True):
            ValTest = 1
        elif (isinstance(Node, ast.Try) == True):
            ValTest = 1

        if ValTest == 1:
            return True
        else:
            return False

    @staticmethod
    def CallsCases(functionNode):
        callsNodes = []
        callsbyexp = []
        callsbyasssign = []
        InAttrCalls = []
        allcallscase = []
        callsNodes = ASTPerser.RecursiveNode(functionNode)
        callsbyexp = ASTPerser.CallsByExpr(functionNode)
        callsbyasssign = ASTPerser.CallsByAssign(functionNode)
        InAttrCalls = ASTPerser.Get_calls_inAtt(functionNode)

        allcallscase = callsNodes + InAttrCalls + callsbyasssign + callsbyexp

        return allcallscase

    @staticmethod
    def CallsByExpr(functionNode):
        CallFunc = []
        y = ASTPerser.Get_Expr_Node(functionNode)
        for arg in y:
            if isinstance(arg.value, ast.Call):
                if isinstance(arg.value.func, ast.Attribute):
                    CallFunc += [arg.value.func.attr]
                else:
                    CallFunc += [arg.value.func.id]
        return CallFunc

    @staticmethod
    def CallsByAssign(functionNode):

        CallFunc = []

        x = ASTPerser.Get_Assign_Node(functionNode)
        for element in x:
            if isinstance(element.value, ast.Call):
                if isinstance(element.value.func, ast.Attribute):
                    CallFunc += [element.value.func.attr]

        return CallFunc

    @staticmethod
    def Get_calls_inAtt(functionNode):
        CallName = []

        x = [m for m in functionNode.body if isinstance(m, ast.Call)]

        for arg in x:
            if isinstance(arg.func, ast.Attribute):
                if isinstance(arg.func.value, ast.Name):
                    CallName += [arg.func.value.attr]

        return CallName

    @staticmethod
    def getCallsFunction(functionNode):
        CallFunc = []
        listefunc = []
        bool = False
        listefunc = ASTPerser.AllCalls(functionNode)


        for m in listefunc:
            bool = ASTPerser.IsExisteInListeNodes(m)
            if bool == True:

                CallFunc.append(m)

        return CallFunc

    @staticmethod
    def IsExisteInListeNodes(element):
        List = []
        count = 0
        for i in methods_functions:
            List += [i.name]

        for i in List:
            if element == i:
                count = count + 1
        if count == 0:
            return False
        else:
            return True


