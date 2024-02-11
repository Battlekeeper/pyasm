import ast

class PyasmTypeChecker():
    def __init__(self, tree, source_lines):
        self.tree = tree
        self.source_lines = source_lines
        self.functions = dict()
        self.functions["float"] = "float"
        self.functions["int"] = "int"
        self.arguments = dict()
        self.variables = dict()

    def allocate_variables(self, body: ast.stmt, assignType:str = None) -> dict:
        variables = dict()
        for node in body.body:
            if isinstance(node, ast.AnnAssign):
                variables[node.target.id] = node.annotation.id
            else:
                if "body" in node._fields:
                    variables.update(self.allocate_variables(node))
            if "orelse" in node._fields:
                for node in node.orelse:
                    if isinstance(node, ast.AnnAssign):
                        variables[node.target.id] = node.annotation.id
                    else:
                        if "body" in node._fields:
                            variables.update(self.allocate_variables(node))
        return variables

    def Handle_Name(self, node:ast.Name, variables:dict):
        return variables[node.id]

    def Handle_BinOp(self, node:ast.BinOp):
        leftType = None
        rightType = None

        if isinstance(node.left, ast.Constant):
            leftType = self.Handle_Constant(node.left.value)
        elif isinstance(node.left, ast.BinOp):
            leftType = self.Handle_BinOp(node.left)
        elif isinstance(node.left, ast.Name):
            leftType = self.Handle_Name(node.left)

        if isinstance(node.right, ast.Constant):
            rightType = self.Handle_Constant(node.right.value)
        elif isinstance(node.right, ast.BinOp):
            rightType = self.Handle_BinOp(node.right)
        elif isinstance(node.right, ast.Name):
            rightType = self.Handle_Name(node.right)

        if leftType == "float" or rightType == "float":
            return "float"
        else:
            return "int"
        
    def Handle_Constant(self, value):
        if isinstance(value, float):
            return "float"
        elif isinstance(value, int):
            return "int"


    def Print_Error(self, node, type, assignedType):
        print(f"Type Error:\n\tTried to assign {assignedType} to {type} at line {node.lineno}: {self.source_lines[node.lineno - 1][node.col_offset:node.end_col_offset].strip()}\n")
        pass

    def Handle_AnnAssign(self, node:ast.AnnAssign, variables:dict):
        if isinstance(node.value, ast.Call):
            if node.annotation.id != self.functions[node.value.func.id]:
                self.Print_Error(node, node.annotation.id, self.functions[node.value.func.id])
        elif isinstance(node.value, ast.BinOp):
            if node.annotation.id != self.Handle_BinOp(node.value):
                self.Print_Error(node, node.annotation.id, self.Handle_BinOp(node.value))
        elif isinstance(node.value, ast.Constant):
            if node.annotation.id != self.Handle_Constant(node.value.value):
                self.Print_Error(node, node.annotation.id, self.Handle_Constant(node.value.value))
        elif isinstance(node.value, ast.Name):
            if node.annotation.id != self.Handle_Name(node.value, variables):
                self.Print_Error(node, node.annotation.id, self.Handle_Name(node.value, variables))
    
    def Handle_Call(self, node:ast.Call, variables:dict):
        if node.func.id == "syscall":
            return
        for index,arg in enumerate(node.args):
            if isinstance(arg, ast.Call):
                if self.Handle_Call(arg, variables) != self.arguments[node.func.id][index]:
                    self.Print_Error(node, self.arguments[node.func.id][index], self.functions[arg.func.id])
            elif isinstance(arg, ast.BinOp):
                if self.Handle_BinOp(arg) != self.arguments[node.func.id][index]:
                    self.Print_Error(node, self.arguments[node.func.id][index], self.Handle_BinOp(arg))
            elif isinstance(arg, ast.Constant):
                if self.Handle_Constant(arg.value) != self.arguments[node.func.id][index]:
                    self.Print_Error(node, self.arguments[node.func.id][index], self.Handle_Constant(arg.value))
            elif isinstance(arg, ast.Name):
                if self.Handle_Name(arg, variables) != self.arguments[node.func.id][index]:
                    self.Print_Error(node, self.arguments[node.func.id][index], self.Handle_Name(arg))
        return self.functions[node.func.id]

    def Handle_Body(self, node, variables:dict):
        for body_node in node.body:
            if isinstance(body_node, ast.AnnAssign):
                self.Handle_AnnAssign(body_node, variables)
            if isinstance(body_node, ast.Expr):
                if isinstance(body_node.value, ast.Call):
                    self.Handle_Call(body_node.value, variables)
                    
                

    def Handle_FunctionDef(self, node:ast.FunctionDef):
        self.functions[node.name] = node.returns.id
        self.arguments[node.name] = []
        
        for arg in node.args.args:
            self.arguments[node.name].append(arg.annotation.id)

        self.Handle_Body(node, self.allocate_variables(node))
        pass

    def check(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.Handle_FunctionDef(node)