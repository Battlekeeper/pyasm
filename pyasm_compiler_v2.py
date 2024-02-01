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

def Handle_FunctionDef(stmt: ast.FunctionDef):

    global assembly_text
    stack_size = 8
    full_stack_size = None
    returnlabel = f"return{stmt.name}"

    scope_variables = dict()
    scope_variables.update(allocate_variables(stmt))

    for name in scope_variables:
        if scope_variables[name] == "int" or scope_variables[name] == "float":
            stack_size += 4
    full_stack_size = stack_size

    for arg in stmt.args.args:
        scope_variables[arg.arg] = arg.annotation.id

    
    #setup function and stack frame
    assembly_text += f"{stmt.name}:\n"
    assembly_text += f"addi $sp, $sp, -{stack_size} # allocate stack\n"           #allocate stack
    assembly_text += f"sw $fp, {stack_size - 4}($sp) # save old frame pointer\n"  #save old frame pointer
    assembly_text += f"move $fp, $sp # set new frame pointer\n"                   #set new frame pointer
    assembly_text += f"sw $ra, {stack_size - 8}($sp) # save return address\n"    #save return address
    stack_size -= 8
    
    # assign variables stack pointers
    for name in scope_variables:
        if scope_variables[name] == "int" or scope_variables[name] == "float":
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
    Handle_Body(stmt.body, scope_variables, returnlabel)

    #set return variables if they exist
    assembly_text += f"{returnlabel}:\n"

    #clear stack and return
    assembly_text += f"lw $fp, {full_stack_size - 4}($sp) # restore old frame pointer\n" #restore old frame pointer
    assembly_text += f"lw $ra, {full_stack_size - 8}($sp) # restore return address\n" #restore return address
    assembly_text += f"addi $sp, $sp, {full_stack_size} # deallocate stack\n" #deallocate stack
    assembly_text += f"jr $ra # return\n"
    assembly_text += f"\n\n"

def Handle_BinOp(stmt: ast.BinOp, scope_variables: dict, assignType: str):
    global assembly_text
    print(scope_variables)
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
        raise NotImplementedError("Call not implemented")
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
        raise NotImplementedError("Call not implemented")
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

    

def Handle_Value(stmt: ast.stmt, scope_variables: dict, assignType: str):
    global assembly_text
    if isinstance(stmt, ast.BinOp):
        Handle_BinOp(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Name):
        raise NotImplementedError("Name not implemented")
        Handle_Name(stmt, scope_variables, assignType)
    elif isinstance(stmt, ast.Constant):
        Handle_Constant(stmt, scope_variables, assignType)
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


def Handle_Body(body: list[ast.stmt], scope_variables: dict, returnlabel: str):
    for stmt in body:
        if isinstance(stmt, ast.FunctionDef):
            Handle_FunctionDef(stmt)
        elif isinstance(stmt, ast.AnnAssign):
            Handle_AnnAssign(stmt, scope_variables, returnlabel)
        elif isinstance(stmt, ast.ImportFrom):
            pass
        else:
            raise Exception(f"Error: Unknown statement {stmt}")

Handle_Body(tree.body, dict, "")

open(output_file, "w").write(assembly_data + assembly_text)