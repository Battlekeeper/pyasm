import ast
import os
import sys
import argparse
from typechecker import PyasmTypeChecker 


parser = argparse.ArgumentParser()
parser.add_argument('-raw', action='store_true', help="Output raw mips assembly without pseudo-instructions", default=False, required=False)
parser.add_argument('-nocomments', action='store_true', help="Output assembly without comments", default=False, required=False)
parser.add_argument('-tree', action='store_true', help="Output abstract syntax tree to tree.py", default=False, required=False)
parser.add_argument('-treeverbose', action='store_true', help="Verbose output of abstract syntax tree to tree.py", default=False, required=False)



parser.add_argument('source', type=str, help="The source file to compile")
parser.add_argument('out', type=str, help="The output file to write the assembly to", default="out.s")

options = parser.parse_args()

variables = dict()
file_data = open(options.source).read()

file_lines = file_data.splitlines()
line_number = 0
for line_number, line in enumerate(file_lines, start=1):
    if "std_lib" in line:
        break

file_lines[line_number-1] = open("std_lib.py").read().replace("def syscall(a: int = 0, b:int = 0) -> void:\n    pass", "")
file_data = "\n".join(file_lines)


source_lines = file_data.split("\n")
tree = ast.parse(file_data)

typeChecker = PyasmTypeChecker(tree, source_lines)
typeChecker.check()


if options.tree or options.treeverbose:
    tree_dump = ast.dump(tree, indent=4, include_attributes=options.treeverbose)
    open("tree.py", "w").write(tree_dump)


assembly_data = ".data\n"
assembly_text = ".text\n.globl main\n"


cast_functions = ["float", "int"]

functions = dict()
functions["float"] = "float"
functions["int"] = "int"


functions_args = dict()
functions_args["float"] = ["int"]
functions_args["int"] = ["float"]


global_variables = dict()

if_stmt_counter = 0
while_stmt_counter = 0


def isBinOpFloat(stmt: ast.BinOp, scope_variables: dict):
    if isinstance(stmt.left, ast.BinOp):
        if isBinOpFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Call):
        if isCallFloat(stmt.left):
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
        if isCallFloat(stmt.right):
            return True
    elif isinstance(stmt.right, ast.Constant):
        if isinstance(stmt.right.value, float):
            return True
    elif isinstance(stmt.right, ast.Name):
        if scope_variables[stmt.right.id] == "float":
            return True

    return False

def isCallFloat(stmt: ast.Call):
    if stmt.func.id in functions:
        if functions[stmt.func.id] == "float":
            return True
    return False

def isCompareFloat(stmt: ast.Compare, scope_variables: dict):
    if isinstance(stmt.left, ast.BinOp):
        if isBinOpFloat(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Call):
        if isCallFloat(stmt.left):
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
        if isCallFloat(stmt.comparators[0]):
            return True
    elif isinstance(stmt.comparators[0], ast.Constant):
        if isinstance(stmt.comparators[0].value, float):
            return True
    elif isinstance(stmt.comparators[0], ast.Name):
        if scope_variables[stmt.comparators[0].id] == "float":
            return True
    return False

def allocate_variables(body: ast.stmt, assignType:str = None) -> dict:
    variables = dict()
    for node in body.body:
        if isinstance(node, ast.AnnAssign):
            variables[node.target.id] = node.annotation.id      
            if (isinstance(node.value, ast.BinOp)):
                if lookFor2BinOps(node.value):
                    variables["lbin"] = node.annotation.id
                    variables["rbin"] = node.annotation.id
        elif isinstance(node, ast.Return):
            if (isinstance(node.value, ast.BinOp)):
                if lookFor2BinOps(node.value):
                    variables["lbin"] = assignType
                    variables["rbin"] = assignType
        else:
            if "body" in node._fields:
                variables.update(allocate_variables(node))
        if "orelse" in node._fields:
            for node in node.orelse:
                if isinstance(node, ast.AnnAssign):
                    variables[node.target.id] = node.annotation.id
                    if (isinstance(node.value, ast.BinOp)):
                        if lookFor2BinOps(node.value):
                            variables["lbin"] = node.annotation.id
                            variables["rbin"] = node.annotation.id
                elif isinstance(node, ast.Return):
                    if (isinstance(node.value, ast.BinOp)):
                        if lookFor2BinOps(node.value):
                            variables["lbin"] = assignType
                            variables["rbin"] = assignType
                else:
                    if "body" in node._fields:
                        variables.update(allocate_variables(node))
    return variables

def lookFor2BinOps(binOp: ast.BinOp) -> True:
    if isinstance(binOp.left, ast.BinOp) and isinstance(binOp.right, ast.BinOp):
        return True
    elif isinstance(binOp.left, ast.BinOp):
        if (binOp.left.left, ast.BinOp) or (binOp.left.right, ast.BinOp):
            return True
        return lookFor2BinOps(binOp.left)
    elif isinstance(binOp.right, ast.BinOp):
        if (binOp.right.left, ast.BinOp) or (binOp.right.right, ast.BinOp):
            return True
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

def checkFloatBitWise(stmt: ast.BinOp, scope_variables: dict) -> bool:
    if isinstance(stmt.left, ast.BinOp):
        if checkFloatBitWise(stmt.left, scope_variables):
            return True
    elif isinstance(stmt.left, ast.Call):
        if isCallFloat(stmt.left):
            return True
    elif isinstance(stmt.left, ast.Constant):
        if isinstance(stmt.left.value, float):
            return True
    elif isinstance(stmt.left, ast.Name):
        if scope_variables[stmt.left.id][0] == "float":
            return True

    if isinstance(stmt.right, ast.BinOp):
        if checkFloatBitWise(stmt.right, scope_variables):
            return True
    elif isinstance(stmt.right, ast.Call):
        if isCallFloat(stmt.right):
            return True
    elif isinstance(stmt.right, ast.Constant):
        if isinstance(stmt.right.value, float):
            return True
    elif isinstance(stmt.right, ast.Name):
        if scope_variables[stmt.right.id][0] == "float":
            return True

    return False

def Handle_FunctionDef(stmt: ast.FunctionDef, level:int):
    global assembly_text
    global functions
    global global_variables

    functions[stmt.name] = stmt.returns.id
    functions_args[stmt.name] = []

    stack_size = 8
    full_stack_size = None
    returnlabel = f"return{stmt.name}"

    scope_variables = dict()
    scope_variables.update(allocate_variables(stmt, stmt.returns.id))

    for name in scope_variables:
        if scope_variables[name] == "int" or scope_variables[name] == "float":
            stack_size += 4

    for arg in stmt.args.args:
        functions_args[stmt.name].append(arg.annotation.id)
        scope_variables[arg.arg] = arg.annotation.id
        if scope_variables[arg.arg] == "int" or scope_variables[arg.arg] == "float":
            stack_size += 4
    
    if bodyHasIfStmt(stmt.body) or bodyHasWhileStmt(stmt.body):
        stack_size += 4
        scope_variables["cmpr"] = "void"
    
    full_stack_size = stack_size

    args_string = ""
    for arg in stmt.args.args:
        args_string += f"{arg.arg}: {arg.annotation.id}, "
    args_string = args_string[:-2]

    if len(stmt.args.args) == 0:
        args_string = "void"

    #setup function and stack frame
    assembly_text += f"{stmt.name}: # {args_string} -> {stmt.returns.id}\n"
    assembly_text += f"addi $sp, $sp, -{stack_size} # allocate stack {list(scope_variables.keys()) + ['$ra', '$fp']} total of {full_stack_size} bytes\n"           #allocate stack
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
            assembly_text += f"sw $a{index}, {var[1]}($fp) # store argument {arg.arg}\n"
        elif var[0] == "float":
            assembly_text += f"swc1 $f{index + 12}, {var[1]}($fp) # store argument {arg.arg}\n"
    
    for child in stmt.body:
        if isinstance(child, ast.Global):
            for name in child.names:
                scope_variables[name] = global_variables[name]
    
    # walk rest of body tree
    Handle_Body(stmt.body, scope_variables, returnlabel, stmt.returns.id, level + 1)

    #set return variables if they exist
    assembly_text += f"{returnlabel}:\n"

    #clear stack and return
    assembly_text += f"lw $fp, {full_stack_size - 4}($sp) # restore old frame pointer\n" #restore old frame pointer
    assembly_text += f"lw $ra, {full_stack_size - 8}($sp) # restore return address\n" #restore return address
    assembly_text += f"addi $sp, $sp, {full_stack_size} # deallocate stack\n" #deallocate stack
    assembly_text += f"jr $ra # return from function by jumping to the pointer in $ra\n"
    assembly_text += f"\n\n"

def Handle_Call(stmt: ast.Call, scope_variables: dict, assignType: str):
    global assembly_text

    if stmt.func.id == "syscall":
        for index,arg in enumerate(stmt.args):
            if isinstance(arg, ast.Name):
                if scope_variables[arg.id][0] == "int":
                    if index == 0:
                        assembly_text += f"lw $v{index}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack\n"
                    else:
                        assembly_text += f"lw $a{index - 1}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack\n"
                elif scope_variables[arg.id][0] == "float":
                    assembly_text += f"lwc1 $f{index + 11}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack\n"
                elif scope_variables[arg.id] == "str":
                    assembly_text += f"la $a{index - 1}, {arg.id} # load pointer of argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.Constant):
                if isinstance(arg.value, int):
                    if index == 0:
                        assembly_text += f"li $v{index}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                    else:
                        assembly_text += f"li $a{index - 1}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                elif isinstance(arg.value, float):
                    assembly_text += f"li.s $f{index + 11}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.BinOp):
                Handle_BinOp(arg, scope_variables, assignType)
                if assignType == "int":
                    if index == 0:
                        assembly_text += f"move $v{index}, $t0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $a{index}\n"
                    else:
                        assembly_text += f"move $a{index - 1}, $t0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $a{index}\n"
                elif assignType == "float":
                    assembly_text += f"mov.s $f{index + 11}, $f0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $f{index + 11}\n"
            elif isinstance(arg, ast.Call):
                Handle_Call(arg, scope_variables, assignType)
                if functions[arg.func.id] == "int":
                    if index != 0:
                        if stmt.func.id in cast_functions:
                            assembly_text += f"move $a{index - 1}, $t0 # move return value of cast {stmt.func.id} to $a{index - 1}\n"
                        else:
                            # v0 already contains the return value of the previous function so no need to move it
                            assembly_text += f"move $a{index - 1}, $v0 # move return value of {stmt.func.id} to $a{index - 1}\n"
                elif functions[arg.func.id] == "float":
                    if not stmt.func.id in cast_functions:
                        # value is already in $f0
                        assembly_text += f"mov.s $f{index + 11}, $f0\n # move return value of {stmt.func.id} to $f{index + 11}"

        assembly_text += f"syscall # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        
    elif stmt.func.id in cast_functions:
        for index,arg in enumerate(stmt.args):
            if isinstance(arg, ast.Name):
                if not isinstance(scope_variables[arg.id], str):
                    if scope_variables[arg.id][0] == "int":
                        assembly_text += f"lw $a{index}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack\n"
                    elif scope_variables[arg.id][0] == "float":
                        assembly_text += f"lwc1 $f{index}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack($fp)\n"
                else:
                    if scope_variables[arg.id] == "int":
                        assembly_text += f"lw $a{index}, {arg.id} # load global argument'{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                    elif scope_variables[arg.id] == "float":
                        assembly_text += f"lwc1 $f{index}, {arg.id} # load global argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                    elif scope_variables[arg.id] == "str":
                        assembly_text += f"la $a{index}, {arg.id} # load pointer of global argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.Constant):
                if isinstance(arg.value, int):
                    assembly_text += f"li $a{index}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                elif isinstance(arg.value, float):
                    assembly_text += f"li.s $f{index}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.BinOp):
                # BinOP handles the conversion automatically here
                Handle_BinOp(arg, scope_variables, functions_args[stmt.func.id][index])
                if functions_args[stmt.func.id][index] == "int":
                    assembly_text += f"move $a{index}, $t0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $a{index}\n"
                elif functions_args[stmt.func.id][index] == "float":
                    # Value already in f0
                    #assembly_text += f"mov.s $f{index + 12}, $f0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $f{index + 12}\n"
                    pass
            elif isinstance(arg, ast.Call):
                        # TODO: Convert return value of function to proper type
                        Handle_Call(arg, scope_variables, assignType)
                        if functions[arg.func.id] == "int":
                            assembly_text += f"move $a{index}, $v0 # move return value of cast {stmt.func.id} to $a{index}\n"
                        elif functions[arg.func.id] == "float":
                            if not stmt.func.id in cast_functions:
                                #value is already in $f0
                                #assembly_text += f"mov.s $f{index + 12}, $f0\n # move return value of {stmt.func.id} to $f{index + 12}"
                                pass

        if stmt.func.id == "float":
            assembly_text += f"mtc1 $a0, $f0 # move integer to coprocessor\n"
            assembly_text += f"cvt.s.w $f0, $f0 # cast int to float {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif stmt.func.id == "int":
            assembly_text += f"cvt.w.s $f0, $f0 # cast float to int {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mfc1 $v0, $f0 # move int from $f0 to integer register {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    else:
        for index,arg in enumerate(stmt.args):
            if isinstance(arg, ast.Name):
                if not isinstance(scope_variables[arg.id], str):
                    if scope_variables[arg.id][0] == "int":
                        assembly_text += f"lw $a{index}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack\n"
                    elif scope_variables[arg.id][0] == "float":
                        assembly_text += f"lwc1 $f{index + 12}, {scope_variables[arg.id][1]}($fp) # load argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' from stack($fp)\n"
                else:
                    if scope_variables[arg.id] == "int":
                        assembly_text += f"lw $a{index}, {arg.id} # load global argument'{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                    elif scope_variables[arg.id] == "float":
                        assembly_text += f"lwc1 $f{index + 12}, {arg.id} # load global argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                    elif scope_variables[arg.id] == "str":
                        assembly_text += f"la $a{index}, {arg.id} # load pointer of global argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.Constant):
                if isinstance(arg.value, int):
                    assembly_text += f"li $a{index}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
                elif isinstance(arg.value, float):
                    assembly_text += f"li.s $f{index + 12}, {arg.value} # load immediate argument '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}'\n"
            elif isinstance(arg, ast.BinOp):
                # BinOP handles the conversion automatically here
                Handle_BinOp(arg, scope_variables, functions_args[stmt.func.id][index])
                if functions_args[stmt.func.id][index] == "int":
                    assembly_text += f"move $a{index}, $t0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $a{index}\n"
                elif functions_args[stmt.func.id][index] == "float":
                    assembly_text += f"mov.s $f{index + 12}, $f0 # move result of '{source_lines[arg.lineno - 1][arg.col_offset:arg.end_col_offset].strip()}' to $f{index + 12}\n"
            elif isinstance(arg, ast.Call):
                Handle_Call(arg, scope_variables, assignType)
                if functions[arg.func.id] == "int":
                    if stmt.func.id in cast_functions:
                        assembly_text += f"move $a{index}, $t0 # move return value of cast {stmt.func.id} to $a{index}\n"
                    else:
                        # v0 already contains the return value of the previous function so no need to move it
                        assembly_text += f"move $a{index}, $v0 # move return value of {stmt.func.id} to $a{index}\n"
                elif functions[arg.func.id] == "float":
                    if not stmt.func.id in cast_functions:
                        # value is already in $f0
                        assembly_text += f"mov.s $f{index + 12}, $f0\n # move return value of {stmt.func.id} to $f{index + 12}"
        assembly_text += f"jal {stmt.func.id} # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"

def Handle_BinOp(stmt: ast.BinOp, scope_variables: dict, assignType: str):
    global assembly_text

    if checkFloatBitWise(stmt, scope_variables) and stmt.op in [ast.LShift, ast.RShift(), ast.BitOr(), ast.BitXor(), ast.BitAnd()]:
        print(f"Error: Cannot perform bitwise operations on floating point numbers at line {stmt.lineno} : {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}")
        sys.exit(1)

    # load values into proper registers
    if isinstance(stmt.left, ast.BinOp):
        Handle_BinOp(stmt.left, scope_variables, assignType)
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"sw $t0, {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"swc1 $f0, {scope_variables['lbin'][1]}($fp)\n"
    if isinstance(stmt.right, ast.BinOp):
        Handle_BinOp(stmt.right, scope_variables, assignType)
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"sw $t0, {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"swc1 $f0, {scope_variables['rbin'][1]}($fp)\n"
        else:
            if assignType == "int":
                assembly_text += f"move $t1, $t0\n"
            elif assignType == "float":
                assembly_text += f"mov.s $f1, $f0\n"

    # TODO: fix type casts for left and right sites
    if isinstance(stmt.left, ast.Call):
        Handle_Call(stmt.left, scope_variables, assignType)
        assembly_text += f"move $t0, $v0 # move return value of {stmt.left.func.id} to $t0\n"
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"sw $t0, {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"swc1 $f0, {scope_variables['lbin'][1]}($fp)\n"
    if isinstance(stmt.right, ast.Call):
        Handle_Call(stmt.right, scope_variables, assignType)
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"move $t0, $v0 # move return value of {stmt.right.func.id} to $t0\n"
                assembly_text += f"sw, $t0, {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"mov.s $f0, $f0 # move return value of {stmt.right.func.id} to $f0\n"
                assembly_text += f"swc1 $f0, {scope_variables['rbin'][1]}($fp)\n"
        else:
            if assignType == "int":
                assembly_text += f"move $t1, $v0 # move result of {stmt.right.func.id} to $t1\n"
            elif assignType == "float":
                assembly_text += f"mov.s $f1, $f0 # move result of {stmt.right.func.id} to $f1\n"


    if isinstance(stmt.left, ast.Name):
        Handle_Name(stmt.left, scope_variables, assignType, "0")
    elif isinstance(stmt.left, ast.Constant):
        Handle_Constant(stmt.left, scope_variables, assignType, "0")
    elif isinstance(stmt.left, ast.Call):
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"lw $t0, {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"lwc1 $f0, {scope_variables['lbin'][1]}($fp)\n"
    elif isinstance(stmt.left, ast.BinOp):
        if "lbin" in scope_variables:
            if scope_variables["lbin"][0] == "int":
                assembly_text += f"lw $t0, {scope_variables['lbin'][1]}($fp)\n"
            elif scope_variables["lbin"][0] == "float":
                assembly_text += f"lwc1 $f0, {scope_variables['lbin'][1]}($fp)\n"

    if isinstance(stmt.right, ast.Name):
        Handle_Name(stmt.right, scope_variables, assignType, "1")
    elif isinstance(stmt.right, ast.Constant):
        Handle_Constant(stmt.right, scope_variables, assignType, "1")
    elif isinstance(stmt.right, ast.Call):
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"lw $t1, {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"lwc1 $f1, {scope_variables['rbin'][1]}($fp)\n"
    elif isinstance(stmt.right, ast.BinOp):
        if "rbin" in scope_variables:
            if scope_variables["rbin"][0] == "int":
                assembly_text += f"lw $t1, {scope_variables['rbin'][1]}($fp)\n"
            elif scope_variables["rbin"][0] == "float":
                assembly_text += f"lwc1 $f1, {scope_variables['rbin'][1]}($fp)\n"
    
    # perform operation
    if isinstance(stmt.op, ast.Add):
        if assignType == "int":
            assembly_text += f"add $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif assignType == "float":
            assembly_text += f"add.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.Sub):
        if assignType == "int":
            assembly_text += f"sub $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif assignType == "float":
            assembly_text += f"sub.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.Mult):
        if assignType == "int":
            assembly_text += f"mul $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mflo $t0 # move integer result of multiplication to $t0\n"
        elif assignType == "float":
            assembly_text += f"mul.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.Div):
        if assignType == "int":
            assembly_text += f"div $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mflo $t0 # move integer result of division to $t0\n"
        elif assignType == "float":
            assembly_text += f"div.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            #assembly_text += f"mflo $f0 # move floating point result of division to $f0\n"
    elif isinstance(stmt.op, ast.FloorDiv):
        if assignType == "int":
            assembly_text += f"div $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mflo $t0 # move integer result of division to $t0\n"
        elif assignType == "float":
            assembly_text += f"div.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"cvt.w.s $f0, $f0 # convert float to int to floor it\n"
            assembly_text += f"cvt.s.w $f0, $f0 # convert int back to a float\n"
    elif isinstance(stmt.op, ast.Mod):
        if assignType == "int":
            assembly_text += f"div $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mfhi $t0 # move integer remainder of division to $t0\n"
        elif assignType == "float":
            assembly_text += f"div.s $f0, $f0, $f1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mfhi $f0\n # move floating point remainder of division to $f0"
    elif isinstance(stmt.op, ast.LShift):
        assembly_text += f"sll $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.RShift):
        assembly_text += f"srl $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.BitOr):
        assembly_text += f"or $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.BitXor):
        assembly_text += f"xor $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.BitAnd):
        assembly_text += f"and $t0, $t0, $t1 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"

def Handle_Constant(stmt: ast.Constant, scope_variables: dict, assignType: str, reg = "0"):
    global assembly_text
    if isinstance(stmt.value, int):
        assembly_text += f"li $t{reg}, {stmt.value} # load immediate value {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        if assignType == "float":
            assembly_text += f"mtc1 $t{reg}, $f{reg} # move {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to coprocessor\n"
            assembly_text += f"cvt.s.w $f{reg}, $f{reg} # convert {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to a float\n"
    elif isinstance(stmt.value, float):
        assembly_text += f"li.s $f{reg}, {stmt.value} # load immediate value {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        if assignType == "int":
            assembly_text += f"cvt.w.s $f{reg}, $f{reg} # convert {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to an int\n"
            assembly_text += f"mfc1 $t{reg}, $f{reg} # move {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} from coprocessor\n"

def Handle_Compare(stmt: ast.Compare, scope_variables: dict, assignType: str):
    global assembly_text

    assignType =  "int"
    if isCompareFloat(stmt, scope_variables):
        assignType = "float"
    
    Handle_Value(stmt.comparators[0], scope_variables, assignType)
    if assignType == "int":
        assembly_text += f"sw $t0, {scope_variables['cmpr'][1]}($fp) # save right side of compare to stack: {source_lines[stmt.comparators[0].lineno - 1][stmt.comparators[0].col_offset:stmt.comparators[0].end_col_offset].strip()}\n"
    elif assignType == "float":
        assembly_text += f"swc1 $f0, {scope_variables['cmpr'][1]}($fp) # save right side of compare to stack: {source_lines[stmt.comparators[0].lineno - 1][stmt.comparators[0].col_offset:stmt.comparators[0].end_col_offset].strip()}\n"
    
    Handle_Value(stmt.left, scope_variables, assignType)

    if assignType == "int":
        assembly_text += f"lw $t1, {scope_variables['cmpr'][1]}($fp) # load right side of compare from stack: {source_lines[stmt.comparators[0].lineno - 1][stmt.comparators[0].col_offset:stmt.comparators[0].end_col_offset].strip()}\n"
    elif assignType == "float":
        assembly_text += f"lwc1 $f1, {scope_variables['cmpr'][1]}($fp) # save right side of compare from stack: {source_lines[stmt.comparators[0].lineno - 1][stmt.comparators[0].col_offset:stmt.comparators[0].end_col_offset].strip()}\n"

    if (len(stmt.ops) > 1 or stmt.ops == 0):
        print(f"Compiler Error: Unsupported number of comparators in if statement at line {stmt.lineno}")
        exit(1)

def Handle_Name(stmt: ast.Name, scope_variables: dict, assignType: str, reg = "0"):
    global assembly_text
    if scope_variables[stmt.id][0] == "int":
        assembly_text += f"lw $t{reg}, {scope_variables[stmt.id][1]}($fp) # load variable {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} from stack\n"
        if assignType == "float":
            assembly_text += f"mtc1 $t{reg}, $f{reg} # move {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to coprocessor\n"
            assembly_text += f"cvt.s.w $f{reg}, $f{reg} # convert {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to float\n"
    elif scope_variables[stmt.id][0] == "float":
        assembly_text += f"lwc1 $f{reg}, {scope_variables[stmt.id][1]}($fp) # load variable {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} from stack\n"
        if assignType == "int":
            assembly_text += f"cvt.w.s $f{reg}, $f{reg} # convert {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} to int\n"
            assembly_text += f"mfc1 $t{reg}, $f{reg} # move {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} from coprocessor\n"

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
        if (stmt.func.id in functions):
            if (functions[stmt.func.id] == "int"):
                assembly_text += f"move $t0, $v0 # move return value of {stmt.func.id} to $t0\n"
    elif isinstance(stmt, ast.Compare):
        Handle_Compare(stmt, scope_variables, assignType)
    else:
        raise Exception(f"Error: Unknown value {stmt}")
    pass

def Handle_AnnAssign(stmt: ast.AnnAssign, scope_variables: dict, returnlabel: str, level:int):
    global assembly_text
    global assembly_data
    global global_variables

    if level != 0:
        Handle_Value(stmt.value, scope_variables, stmt.annotation.id)

        if stmt.annotation.id == "int":
            assembly_text += f"sw $t0, {scope_variables[stmt.target.id][1]}($fp) # assign {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} in stack\n"
        elif stmt.annotation.id == "float":
            assembly_text += f"swc1 $f0, {scope_variables[stmt.target.id][1]}($fp) # assign {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} in stack\n"
        pass
    else:
        if (not isinstance(stmt.value, ast.Constant)):
            print(f"Compiler Error: Global variable {stmt.target.id} must be initialized with a constant at line {stmt.lineno}")
            exit(1)
        if stmt.annotation.id == "int":
            assembly_data += f"{stmt.target.id}: .word {int(stmt.value.value)}\n"
        elif stmt.annotation.id == "float":
            assembly_data += f"{stmt.target.id}: .float {float(stmt.value.value)}\n"
        elif stmt.annotation.id == "str":
            assembly_data += f"{stmt.target.id}: .asciiz \"{stmt.value.value}\"\n"
        global_variables[stmt.target.id] = stmt.annotation.id
        
def Handle_AugAssign(stmt: ast.AnnAssign, scope_variables: dict, returnlabel: str, level:int):
    global assembly_text
    global assembly_data
    global global_variables

    Handle_Value(stmt.value, scope_variables, scope_variables[stmt.target.id][0])


    if scope_variables[stmt.target.id][0] == "int":
        assembly_text += f"lw $t1, {scope_variables[stmt.target.id][1]}($fp) # load argument '{source_lines[stmt.target.lineno - 1][stmt.target.col_offset:stmt.target.end_col_offset].strip()}' from stack\n"
    elif scope_variables[stmt.target.id][0] == "float":
        assembly_text += f"lwc1 $f1, {scope_variables[stmt.target.id][1]}($fp) # load argument '{source_lines[stmt.target.lineno - 1][stmt.target.col_offset:stmt.target.end_col_offset].strip()}' from stack\n"

    if  isinstance(stmt.op, ast.Add):
        if scope_variables[stmt.target.id][0] == "int":
            assembly_text += f"add $t0, $t1, $t0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif scope_variables[stmt.target.id][0] == "float":
            assembly_text += f"add.s $f0, $f1, $f0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.Sub):
        if scope_variables[stmt.target.id][0] == "int":
            assembly_text += f"sub $t0, $t1, $t0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif scope_variables[stmt.target.id][0] == "float":
            assembly_text += f"sub.s $f0, $f1, $f0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.op, ast.Mult):
        if scope_variables[stmt.target.id][0] == "int":
            assembly_text += f"mul $t0, $t1, $t0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mflo $t0 # move integer result of multiplication to $t0\n"
        elif scope_variables[stmt.target.id][0] == "float":
            assembly_text += f"mul.s $f0, $f1, $f0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            #assembly_text += f"mflo $f0 # move floating point result of multiplication to $f0\n"
    elif isinstance(stmt.op, ast.Div):
        if scope_variables[stmt.target.id][0] == "int":
            assembly_text += f"div $t0, $t1, $t0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            assembly_text += f"mflo $t0 # move integer result of division to $f0\n"
        elif scope_variables[stmt.target.id][0] == "float":
            assembly_text += f"div.s $f0, $f1, $f0 # {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
            #assembly_text += f"mflo $f0\n # move floating point result of division to $f0"
    
    if scope_variables[stmt.target.id][0] == "int":
        assembly_text += f"sw $t0, {scope_variables[stmt.target.id][1]}($fp) # assign {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} in stack\n"
    elif scope_variables[stmt.target.id][0] == "float":
        assembly_text += f"swc1 $f0, {scope_variables[stmt.target.id][1]}($fp) # assign {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()} in stack\n"

def Handle_Return(stmt: ast.Return, scope_variables: dict, returnlabel: str, assignType, level:int):
    global assembly_text
    if isinstance(stmt.value, ast.BinOp):
        Handle_BinOp(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.value, ast.Call):
        Handle_Call(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    elif isinstance(stmt.value, ast.Constant):
        Handle_Constant(stmt.value, scope_variables, assignType)
        if assignType == "int":
            assembly_text += f"move $v0, $t0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
        elif assignType == "float":
            assembly_text += f"mov.s $f0, $f0 # return result: {source_lines[stmt.lineno - 1][stmt.col_offset:stmt.end_col_offset].strip()}\n"
    assembly_text += f"j {returnlabel} # jump to {returnlabel} to clean up function\n"

def Handle_If(stmt: ast.If, scope_variables: dict, returnlabel: str, assignType, level:int):
    global assembly_text
    global if_stmt_counter

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
            assembly_text += f"ble $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"bge $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"bne $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"blt $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"bgt $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"beq $t0, $t1, iffalse{if_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")

    Handle_Body(stmt.body, scope_variables, returnlabel, assignType, level + 1)
    assembly_text += f"j endIf{if_stmt_counter}\n"

    assembly_text += f"iffalse{if_stmt_counter}:\n"
    if len(stmt.orelse) > 0:
        Handle_Body(stmt.orelse, scope_variables, returnlabel, assignType, level + 1)
    assembly_text += f"endIf{if_stmt_counter}:\n"

    if_stmt_counter += 1

def Handle_While(stmt: ast.While, scope_variables: dict, returnlabel: str, assignType, level:int):
    global assembly_text
    global while_stmt_counter

    assembly_text += f"startWhile{while_stmt_counter}:\n"
    Handle_Value(stmt.test, scope_variables, assignType)
    if isCompareFloat(stmt.test, scope_variables):
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"c.le.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"c.lt.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"c.eq.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"c.lt.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"c.le.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1f endwhile{while_stmt_counter}\n"
            pass
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"c.eq.s $f0, $f1 # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
            assembly_text += f"bc1t endwhile{while_stmt_counter}\n"
            pass
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")
    else:
        if (isinstance(stmt.test.ops[0], ast.Gt)):
            assembly_text += f"ble $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.Lt)):
            assembly_text += f"bge $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.Eq)):
            assembly_text += f"bne $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.GtE)):
            assembly_text += f"blt $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.LtE)):
            assembly_text += f"bgt $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        elif (isinstance(stmt.test.ops[0], ast.NotEq)):
            assembly_text += f"beq $t0, $t1, endwhile{while_stmt_counter} # {source_lines[stmt.test.lineno - 1][stmt.test.col_offset:stmt.test.end_col_offset].strip()}\n"
        else:
            raise Exception(f"Error: Unknown comparison in if statement at line {stmt.lineno}")
    Handle_Body(stmt.body, scope_variables, returnlabel, assignType, level + 1)
    assembly_text += f"j startWhile{while_stmt_counter}\n"
    assembly_text += f"endwhile{while_stmt_counter}:\n"

def Handle_Body(body: list[ast.stmt], scope_variables: dict, returnlabel: str, assignType, level = -1):
    global assembly_text
    for stmt in body:
        if isinstance(stmt, ast.FunctionDef):
            Handle_FunctionDef(stmt, level)
        elif isinstance(stmt, ast.AnnAssign):
            Handle_AnnAssign(stmt, scope_variables, returnlabel, level)
        elif isinstance(stmt, ast.AugAssign):
            Handle_AugAssign(stmt, scope_variables, returnlabel, level)
        elif isinstance(stmt, ast.Return):
            Handle_Return(stmt, scope_variables, returnlabel, assignType, level)
        elif isinstance(stmt, ast.If):
            Handle_If(stmt, scope_variables, returnlabel, assignType, level)
        elif isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                Handle_Call(stmt.value, scope_variables, assignType)
                if (stmt.value.func.id in functions):
                    if (functions[stmt.value.func.id] == "int"):
                        assembly_text += f"move $t0, $v0 # move return value of {stmt.value.func.id} to $t0\n"
        elif isinstance(stmt, ast.While):
            Handle_While(stmt, scope_variables, returnlabel, assignType, level)
        elif isinstance(stmt, ast.ImportFrom) or isinstance(stmt, ast.Global) or isinstance(stmt, ast.ClassDef) or isinstance(stmt, ast.Pass):
            pass
        else:
            raise Exception(f"Error: Unknown statement in body {stmt}")

Handle_Body(tree.body, dict, "", "", 0)

full_asm = assembly_data + assembly_text

lines = full_asm.split("\n")

for index, line in enumerate(lines):
    if (index + 1) < len(lines):
        if line.split("#")[0].strip() == "move $t0, $v0":
            if lines[index + 1].split("#")[0].strip() == "move $t0, $v0":
                lines.pop(index + 1)
                pass
        if len(line.split("#")[0].split()) > 0 and len(lines[index + 1].split("#")[0].split()) > 0:
            arr1 = line.split("#")[0].split()
            arr2 = lines[index + 1].split("#")[0].split()
            if arr1[0].strip() == "sw" and arr2[0].strip() == "lw":
                    if arr1[1].strip() == arr2[1].strip() and arr1[2].strip() == arr2[2].strip():
                         lines.pop(index + 1)

if options.raw:
    # replace pseudo instructions with real instructions
    for index, line in enumerate(lines):
        comment = line.split("#")
        if len(comment) > 1:
            comment = "# " + comment[1]
        else:
            comment = ""
        linearr = line.split(" ")
        if linearr[0] == "move":
            lines[index] = f"addu {linearr[1]}, $zero, {linearr[2]} {comment}"
        elif linearr[0] == "li":
            lines[index] = f"ori {linearr[1]}, $zero, {linearr[2]} {comment}"
        elif linearr[0] == "lw":
            pass
    pass

if options.nocomments:
    for index, line in enumerate(lines):
        lines[index] = line.split("#")[0]

open(options.out, "w").write("\n".join(lines))