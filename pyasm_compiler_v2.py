import ast
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python3 pyasm_compiler.py <input_file> <output_file>")
    exit(1)
input_file = sys.argv[1]
output_file = "out.s"
if len(sys.argv) == 3:
    output_file = sys.argv[2]

if not os.path.isfile(input_file):
    print(f"Error: {input_file} does not exist")
    exit(1)

variables = dict()

tree = ast.parse(open(input_file).read())
print("\n" + ast.dump(tree) + "\n")

assembly_data = ".data\n"
assembly_text = ".text\n.globl main\n"


std_functions_asm = dict()
std_functions_asm["print_int"] = [
    [],
    "print_int:\nli $v0, 1\nsyscall\nbne $a1, $zero, print_newline\njr $ra",
]
std_functions_asm["print_float"] = [
    ['float_format: .asciiz "%f"'],
    """print_float:\nli   $v0, 2\nmov.s $f12, $f12\nla   $a0, float_format\nsyscall\nbne $a1, $zero, print_newline\njr   $ra""",
]
std_functions_asm["print_newline"] = [
    [],
    """print_newline:\nli   $v0, 11\nli   $a0, '\\n'\nsyscall\njr   $ra""",
]
std_functions_asm["terminate"] = [
    [],
    "terminate:\nli   $v0, 10\nsyscall",
]

functions = dict()

if_stmt_counter = 0
while_stmt_counter = 0

for func in std_functions_asm:
    for line in std_functions_asm[func][0]:
        assembly_data += f"{line}\n"
    assembly_text += f"{std_functions_asm[func][1]}\n"

def isBinOpFloat(stmt: ast.BinOp, scope_variables: dict):
    if isinstance(stmt.left, ast.BinOp):
        if isBinOpFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Call):
        if isCallFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Constant):
        if isinstance(stmt.left.value, float):
            return True
    elif isinstance(stmt.left, ast.Name):
        if scope_variables[stmt.left.id] == "float":
            return True

    if isinstance(stmt.right, ast.BinOp):
        if isBinOpFloat(stmt.right, scope_variables):
            return True
    elif isinstance(stmt.right, ast.Call):
        if isCallFloat(stmt.right, scope_variables):
            return True
    elif isinstance(stmt.right, ast.Constant):
        if isinstance(stmt.right.value, float):
            return True
    elif isinstance(stmt.right, ast.Name):
        if scope_variables[stmt.right.id] == "float":
            return True

    return False

def isCallFloat(stmt: ast.Call, scope_variables: dict):
    if stmt.func.id in functions:
        if functions[stmt.func.id] == "float":
            return True
    return False

def isCompareFloat(stmt: ast.Compare, scope_variables: dict):
    if isinstance(stmt.left, ast.BinOp):
        if isBinOpFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Call):
        if isCallFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Constant):
        if isinstance(stmt.left.value, float):
            return True
    elif isinstance(stmt.left, ast.Name):
        if scope_variables[stmt.left.id] == "float":
            return True
    
    if isinstance(stmt.comparators[0], ast.BinOp):
        if isBinOpFloat(stmt.comparators[0], scope_variables):
            return True
    elif isinstance(stmt.comparators[0], ast.Call):
        if isCallFloat(stmt.comparators[0], scope_variables):
            return True
    elif isinstance(stmt.comparators[0], ast.Constant):
        if isinstance(stmt.comparators[0].value, float):
            return True
    elif isinstance(stmt.comparators[0], ast.Name):
        if scope_variables[stmt.comparators[0].id] == "float":
            return True
    return False

def allocate_variables(body: ast.stmt) -> dict:
    variables = dict()
    for node in body.body:
        if isinstance(node, ast.AnnAssign):
            variables[node.target.id] = node.annotation.id      
            if (isinstance(node.value, ast.BinOp)):
                if lookFor2BinOps(node.value):
                    variables["lbin"] = node.annotation.id
                    variables["rbin"] = node.annotation.id
        else:
            if "body" in node._fields:
                variables.update(allocate_variables(node))
    return variables

def lookFor2BinOps(binOp: ast.BinOp) -> True:
    if isinstance(binOp.left, ast.BinOp) and isinstance(binOp.right, ast.BinOp):
        return True
    elif isinstance(binOp.left, ast.BinOp):
        return lookFor2BinOps(binOp.left)
    elif isinstance(binOp.right, ast.BinOp):
        return lookFor2BinOps(binOp.right)
    else:
        return False

def bodyHasIfStmt(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, ast.If):
            return True
        else:
            if "body" in stmt._fields:
                if bodyHasIfStmt(stmt.body):
                    return True
    return False

def bodyHasWhileStmt(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, ast.While):
            return True
        else:
            if "body" in stmt._fields:
                if bodyHasWhileStmt(stmt.body):
                    return True
    return False


def Handle_FunctionDef(stmt: ast.FunctionDef):
    global assembly_text
    global functions

    functions[stmt.name] = stmt.returns.id

    stack_size = 8
    full_stack_size = None
    returnlabel = f"return{stmt.name}"

    scope_variables = dict()
    scope_variables.update(allocate_variables(stmt))

    for name in scope_variables:
        if scope_variables[name] == "int" or scope_variables[name] == "float":
            stack_size += 4

    for arg in stmt.args.args:
        scope_variables[arg.arg] = arg.annotation.id
        if scope_variables[arg.arg] == "int" or scope_variables[arg.arg] == "float":
            stack_size += 4
    
    if bodyHasIfStmt(stmt.body) or bodyHasWhileStmt(stmt.body):
        stack_size += 4
        scope_variables["cmpr"] = "void"
    
    full_stack_size = stack_size

    #setup function and stack frame
    assembly_text += f"{stmt.name}:\n"
    assembly_text += f"addi $sp, $sp, -{stack_size} # allocate stack\n"           #allocate stack
    assembly_text += f"sw $fp, {stack_size - 4}($sp) # save old frame pointer\n"  #save old frame pointer
    assembly_text += f"move $fp, $sp # set new frame pointer\n"                   #set new frame pointer
    assembly_text += f"sw $ra, {stack_size - 8}($sp) # save return address\n"    #save return address
    stack_size -= 8
    
    # assign variables stack pointers
    for name in scope_variables:
        if scope_variables[name] == "int" or scope_variables[name] == "float" or name == "cmpr":
            scope_variables[name] = [scope_variables[name], stack_size - 4]
            stack_size -= 4
    
    # assign values to said stack pointers
    for index, arg in enumerate(stmt.args.args):
        var = scope_variables[arg.arg]
        if var[0] == "int":
            assembly_text += f"sw $a{index}, {var[1]}($fp) # store argument {index}\n"
        elif var[0] == "float":
            assembly_text += f"swc1 $f{index + 12}, {var[1]}($fp) # store argument {index}\n"

    # walk rest of body tree
    Handle_Body(stmt.body, scope_variables, returnlabel, stmt.returns.id)

    #set return variables if they exist
    assembly_text += f"{returnlabel}:\n"

    #clear stack and return
    assembly_text += f"lw $fp, {full_stack_size - 4}($sp) # restore old frame pointer\n" #restore old frame pointer
    assembly_text += f"lw $ra, {full_stack_size - 8}($sp) # restore return address\n" #restore return address
    assembly_text += f"addi $sp, $sp, {full_stack_size} # deallocate stack\n" #deallocate stack
    assembly_text += f"jr $ra # return\n"
    assembly_text += f"\n\n"

def Handle_Call(stmt: ast.Call, scope_variables: dict, assignType: str):
    global assembly_text

    for index,arg in enumerate(stmt.args):
        if isinstance(arg, ast.Name):
            if scope_variables[arg.id][0] == "int":
                assembly_text += f"lw $a{index}, {scope_variables[arg.id][1]}($fp)\n"
            elif scope_variables[arg.id][0] == "float":
                assembly_text += f"lwc1 $f{index + 12}, {scope_variables[arg.id][1]}($fp)\n"
        elif isinstance(arg, ast.Constant):
            if isinstance(arg.value, int):
                assembly_text += f"li $a{index}, {arg.value}\n"
            elif isinstance(arg.value, float):
                assembly_text += f"li.s $f{index + 12}, {arg.value}\n"
        elif isinstance(arg, ast.BinOp):
            Handle_BinOp(arg, scope_variables, assignType)
            if assignType == "int":
                assembly_text += f"move $a{index}, $t0\n"
            elif assignType == "float":
                assembly_text += f"mov.s $f{index + 12}, $f0\n"
        elif isinstance(arg, ast.Call):
            Handle_Call(arg, scope_variables, assignType)
            if assignType == "int":
                assembly_text += f"move $a{index}, $v0\n"
            elif assignType == "float":
                assembly_text += f"mov.s $f{index + 12}, $f0\n"        

    assembly_text += f"jal {stmt.func.id}\n"
    assembly_text += f"move $t0, $v0\n"

def Handle_BinOp(stmt: ast.BinOp, scope_variables: dict, assignType: str):
    global assembly_text
    # load values into proper registers
    if isinstance(stmt.left, ast.BinOp):
        Handle_BinOp(stmt.left, scope_variables, assignType)
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"sw $t0 {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"swc1 $f0 {scope_variables['lbin'][1]}($fp)\n"
    if isinstance(stmt.right, ast.BinOp):
        Handle_BinOp(stmt.right, scope_variables, assignType)
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"sw $t0 {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"swc1 $f0 {scope_variables['rbin'][1]}($fp)\n"
        else:
            if assignType == "int":
                assembly_text += f"move $t1, $t0\n"
            elif assignType == "float":
                assembly_text += f"mov.s $f1, $f0\n"


    if isinstance(stmt.left, ast.Name):
        if scope_variables[stmt.left.id][0] == "int":
            assembly_text += f"lw $t0, {scope_variables[stmt.left.id][1]}($fp)\n"
            if assignType == "float":
                assembly_text += f"mtc1 $t0, $f0\n"
                assembly_text += f"cvt.s.w $f0, $f0\n"
        elif scope_variables[stmt.left.id][0] == "float":
            assembly_text += f"lwc1 $f0, {scope_variables[stmt.left.id][1]}($fp)\n"
    elif isinstance(stmt.left, ast.Constant):
        if isinstance(stmt.left.value, int):
            assembly_text += f"li $t0, {stmt.left.value}\n"
            if assignType == "float":
                assembly_text += f"mtc1 $t0, $f0\n"
                assembly_text += f"cvt.s.w $f0, $f0\n"
        elif isinstance(stmt.left.value, float):
            assembly_text += f"li.s $f0, {stmt.left.value}\n"
    elif isinstance(stmt.left, ast.Call):
        Handle_Call(stmt.left, scope_variables, assignType)
        assembly_text += f"move $t0, $v0\n"
        
    elif isinstance(stmt.left, ast.BinOp):
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"lw $t0, {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"lwc1 $f0, {scope_variables['lbin'][1]}($fp)\n"

    if isinstance(stmt.right, ast.Name):
        if scope_variables[stmt.right.id][0] == "int":
            assembly_text += f"lw $t1, {scope_variables[stmt.right.id][1]}($fp)\n"
            if assignType == "float":
                assembly_text += f"mtc1 $t1, $f1\n"
                assembly_text += f"cvt.s.w $f1, $f1\n"
        elif scope_variables[stmt.right.id][0] == "float":
            assembly_text += f"lwc1 $f1, {scope_variables[stmt.right.id][1]}($fp)\n"
    elif isinstance(stmt.right, ast.Constant):
        if isinstance(stmt.right.value, int):
            assembly_text += f"li $t1, {stmt.right.value}\n"
            if assignType == "float":
                assembly_text += f"mtc1 $t1, $f1\n"
                assembly_text += f"cvt.s.w $f1, $f1\n"
        elif isinstance(stmt.right.value, float):
            assembly_text += f"li.s $f1, {stmt.right.value}\n"
    elif isinstance(stmt.right, ast.Call):
        Handle_Call(stmt.left, scope_variables, assignType)
    elif isinstance(stmt.right, ast.BinOp):
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"lw $t1, {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"lwc1 $f1, {scope_variables['rbin'][1]}($fp)\n"
    
    # perform operation
    if isinstance(stmt.op, ast.Add):
        if assignType == "int":
            assembly_text += f"add $t0, $t0, $t1\n"
        elif assignType == "float":
            assembly_text += f"add.s $f0, $f0, $f1\n"
    elif isinstance(stmt.op, ast.Sub):
        if assignType == "int":
            assembly_text += f"sub $t0, $t0, $t1\n"
        elif assignType == "float":
            assembly_text += f"sub.s $f0, $f0, $f1\n"
    elif isinstance(stmt.op, ast.Mult):
        if assignType == "int":
            assembly_text += f"mul $t0, $t0, $t1\n"
            assembly_text += f"mflo $t0\n"
        elif assignType == "float":
            assembly_text += f"mul.s $f0, $f0, $f1\n"
            assembly_text += f"mflo $f0\n"
    elif isinstance(stmt.op, ast.Div):
        if assignType == "int":
            assembly_text += f"div $t0, $t0, $t1\n"
            assembly_text += f"mflo $t0\n"
        elif assignType == "float":
            assembly_text += f"div.s $f0, $f0, $f1\n"
            assembly_text += f"mflo $f0\n"

def Handle_Constant(stmt: ast.Constant, scope_variables: dict, assignType: str):
    global assembly_text
    if isinstance(stmt.value, int):
        assembly_text += f"li $t0, {stmt.value}\n"
        if assignType == "float":
            assembly_text += f"mtc1 $t0, $f0\n"
            assembly_text += f"cvt.s.w $f0, $f0\n"
    elif isinstance(stmt.value, float):
        assembly_text += f"li.s $f0, {stmt.value}\n"
        if assignType == "int":
            assembly_text += f"cvt.w.s $f0, $f0\n"
            assembly_text += f"mfc1 $t0, $f0\n"

def Handle_Compare(stmt: ast.Compare, scope_variables: dict, assignType: str):
    global assembly_text

    assignType =  "int"
    if isCompareFloat(stmt, scope_variables):
        assignType = "float"
    
    Handle_Value(stmt.comparators[0], scope_variables, assignType)
    if assignType == "int":
        assembly_text += f"sw $t0, {scope_variables['cmpr'][1]}($fp)\n"
    elif assignType == "float":
        assembly_text += f"swc1 $f0, {scope_variables['cmpr'][1]}($fp)\n"
    
    Handle_Value(stmt.left, scope_variables, assignType)

    if assignType == "int":
        assembly_text += f"lw $t1, {scope_variables['cmpr'][1]}($fp)\n"
    elif assignType == "float":
        assembly_text += f"lwc1 $f1, {scope_variables['cmpr'][1]}($fp)\n"

    if (len(stmt.ops) > 1 or stmt.ops == 0):
        print(f"Compiler Error: Unsupported number of comparators in if statement at line {stmt.lineno}")
        exit(1)

def Handle_Name(stmt: ast.Name, scope_variables: dict, assignType: str):
    global assembly_text
    if scope_variables[stmt.id][0] == "int":
        assembly_text += f"lw $t0, {scope_variables[stmt.id][1]}($fp)\n"
        if assignType == "float":
            assembly_text += f"mtc1 $t0, $f0\n"
            assembly_text += f"cvt.s.w $f0, $f0\n"
    elif scope_variables[stmt.id][0] == "float":
        assembly_text += f"lwc1 $f0, {scope_variables[stmt.id][1]}($fp)\n"
        if assignType == "int":
            assembly_text += f"cvt.w.s $f0, $f0\n"
            assembly_text += f"mfc1 $t0, $f0\n"

def Handle_Value(stmt: ast.stmt, scope_variables: dict, assignType: str):
    global assembly_text
    if isinstance(stmt, ast.BinOp):
        Handle_BinOp(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Name):
        Handle_Name(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Constant):
        Handle_Constant(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Call):
        Handle_Call(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Compare):
        Handle_Compare(stmt, scope_variables, assignType)
    else:
        raise Exception(f"Error: Unknown value {stmt}")
    pass

def Handle_AnnAssign(stmt: ast.AnnAssign, scope_variables: dict, returnlabel: str):
    global assembly_text

    Handle_Value(stmt.value, scope_variables, stmt.annotation.id)


    if stmt.annotation.id == "int":
        assembly_text += f"sw $t0, {scope_variables[stmt.target.id][1]}($fp)\n"
    elif stmt.annotation.id == "float":
        assembly_text += f"swc1 $f0, {scope_variables[stmt.target.id][1]}($fp)\n"
    pass


def Handle_Return(stmt: ast.Return, scope_variables: dict, returnlabel: str, assignType):
    global assembly_text
    if isinstance(stmt.value, ast.BinOp):
        Handle_BinOp(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0\n"
    elif isinstance(stmt.value, ast.Call):
        Handle_Call(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0\n"
    elif isinstance(stmt.value, ast.Constant):
        Handle_Constant(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0\n"
    assembly_text += f"j {returnlabel}\n"

def Handle_If(stmt: ast.If, scope_variables: dict, returnlabel: str, assignType):
    global assembly_text
    global if_stmt_counter

    assembly_text += f"# if statement\n"
    Handle_Value(stmt.test, scope_variables, assignType)

    if isCompareFloat(stmt.test, scope_variables):
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"c.le.s $f0, $f1\n"
            assembly_text += f"bc1t iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"c.lt.s $f0, $f1\n"
            assembly_text += f"bc1f iffalse{if_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"c.eq.s $f0, $f1\n"
            assembly_text += f"bc1f iffalse{if_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"c.lt.s $f0, $f1\n"
            assembly_text += f"bc1t iffalse{if_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"c.le.s $f0, $f1\n"
            assembly_text += f"bc1f iffalse{if_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"c.eq.s $f0, $f1\n"
            assembly_text += f"bc1t iffalse{if_stmt_counter}\n"
            pass
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")
    else:
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"ble $t0, $t1, iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"bge $t0, $t1, iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"bne $t0, $t1, iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"blt $t0, $t1, iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"bgt $t0, $t1, iffalse{if_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"beq $t0, $t1, iffalse{if_stmt_counter}\n"
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")

    Handle_Body(stmt.body, scope_variables, returnlabel, assignType)
    assembly_text += f"j endIf{if_stmt_counter}\n"

    assembly_text += f"iffalse{if_stmt_counter}:\n"
    if len(stmt.orelse) > 0:
        Handle_Body(stmt.orelse, scope_variables, returnlabel, assignType)
    assembly_text += f"endIf{if_stmt_counter}:\n"

    if_stmt_counter += 1

def Handle_While(stmt: ast.While, scope_variables: dict, returnlabel: str, assignType):
    global assembly_text
    global while_stmt_counter

    assembly_text += f"# while statement\n"
    assembly_text += f"startWhile{while_stmt_counter}:\n"
    Handle_Value(stmt.test, scope_variables, assignType)
    if isCompareFloat(stmt.test, scope_variables):
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"c.le.s $f0, $f1\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"c.lt.s $f0, $f1\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"c.eq.s $f0, $f1\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"c.lt.s $f0, $f1\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"c.le.s $f0, $f1\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"c.eq.s $f0, $f1\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
            pass
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")
    else:
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"ble $t0, $t1, endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"bge $t0, $t1, endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"bne $t0, $t1, endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"blt $t0, $t1, endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"bgt $t0, $t1, endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"beq $t0, $t1, endwhile{while_stmt_counter}\n"
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")
    Handle_Body(stmt.body, scope_variables, returnlabel, assignType)
    assembly_text += f"j startWhile{while_stmt_counter}\n"
    assembly_text += f"endwhile{while_stmt_counter}:\n"





def Handle_Body(body: list[ast.stmt], scope_variables: dict, returnlabel: str, assignType):
    for stmt in body:
        if isinstance(stmt, ast.FunctionDef):
            Handle_FunctionDef(stmt)
        elif isinstance(stmt, ast.AnnAssign):
            Handle_AnnAssign(stmt, scope_variables, returnlabel)
        elif isinstance(stmt, ast.Return):
            Handle_Return(stmt, scope_variables, returnlabel, assignType)
        elif isinstance(stmt, ast.If):
            Handle_If(stmt, scope_variables, returnlabel, assignType)
        elif isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                Handle_Call(stmt.value, scope_variables, assignType)
        elif isinstance(stmt, ast.While):
            Handle_While(stmt, scope_variables, returnlabel, assignType)
        elif isinstance(stmt, ast.ImportFrom):
            pass
        else:
            raise Exception(f"Error: Unknown statement in body {stmt}")

Handle_Body(tree.body, dict, "", "")

open(output_file, "w").write(assembly_data + assembly_text)