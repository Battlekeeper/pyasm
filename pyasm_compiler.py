import ast

variables = dict()
std_functions_asm = dict()
std_functions_asm["print_int"] = [
    [],
    "print_int:\nli $v0, 1\nsyscall\njr $ra",
]
std_functions_asm["print_float"] = [
    ['float_format: .asciiz "%f"'],
    """print_float:\nli   $v0, 2\nmov.s $f12, $f12\nla   $a0, float_format\nsyscall\njr   $ra""",
]
std_functions_asm["print_newline"] = [
    [],
    """print_newline:\nli   $v0, 11\nli   $a0, '\\n'\nsyscall\njr   $ra""",
]
std_functions_asm["terminate"] = [
    [],
    "terminate:\nli   $v0, 10\nsyscall",
]

std_functions = set()
ifstatementId = 0
whileloopid = 0

# Generate MIPS assembly code from AST
tree = ast.parse(open("source.pyasm").read())
print("\n" + ast.dump(tree) + "\n")

assembly_text = ""

def allocate_variables(body) -> dict:
    variables = dict()
    for node in body.body:
        if isinstance(node, ast.AnnAssign):
            variables[node.target.id] = node.annotation.id
        else:
            if "body" in node._fields:
                variables.update(allocate_variables(node))
    return variables

def handle_binop(node: ast.BinOp, varnode:ast.AnnAssign, variables: dict):
    global assembly_text
    target_type = variables[varnode.target.id][0]
    
    left_type = ""
    right_type = ""
    if isinstance(node.left, ast.Constant):
        left_type = "int" if isinstance(node.left.value, int) else "float"
    elif isinstance(node.left, ast.Name):
        left_type = variables[node.left.id][0]
    if isinstance(node.right, ast.Constant):
        right_type = "int" if isinstance(node.right.value, int) else "float"
    elif isinstance(node.right, ast.Name):
        right_type = variables[node.right.id][0]

    if left_type == "int" and right_type == "int":
        if (isinstance(node.left, ast.Constant)):
            assembly_text += f"li $t0, {node.left.value}\n"
        else:
            assembly_text += f"lw $t0, {variables[node.left.id][1]}($fp)\n"

        if (isinstance(node.right, ast.Constant)):
            assembly_text += f"li $t1, {node.right.value}\n"
        else:
            assembly_text += f"lw $t1, {variables[node.right.id][1]}($fp)\n"
        
        if isinstance(node.op, ast.Add):
            assembly_text += f"add $t0, $t0, $t1\n"
        elif isinstance(node.op, ast.Sub):
            assembly_text += f"sub $t0, $t0, $t1\n"
        elif isinstance(node.op, ast.Mult):
            assembly_text += f"mult $t0, $t1\n"
            assembly_text += f"mflo $t0\n"
        elif isinstance(node.op, ast.Div):
            assembly_text += f"div $t0, $t1\n"
            assembly_text += f"mflo $t0\n"
        if target_type == "int":
            assembly_text += f"sw $t0, {variables[varnode.target.id][1]}($fp)\n"
        else:
            assembly_text += f"mtc1 $t0, $f0\n"
            assembly_text += f"cvt.s.w $f0, $f0\n"
            assembly_text += f"swc1 $f0, {variables[varnode.target.id][1]}($fp)\n"
    elif left_type == "float" and right_type == "float":
        if (isinstance(node.left, ast.Constant)):
            assembly_text += f"li.s $f0, {node.left.value}\n"
        else:
            assembly_text += f"lwc1 $f0, {variables[node.left.id][1]}($fp)\n"

        if (isinstance(node.right, ast.Constant)):
            assembly_text += f"li.s $f1, {node.right.value}\n"
        else:
            assembly_text += f"lwc1 $f1, {variables[node.right.id][1]}($fp)\n"
        
        
        if isinstance(node.op, ast.Add):
            assembly_text += f"add.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Sub):
            assembly_text += f"sub.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Mult):
            assembly_text += f"mul.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Div):
            assembly_text += f"div.s $f0, $f0, $f1\n"
        if target_type == "int":
            assembly_text += f"trunc.w.s $f0, $f0\n"
            assembly_text += f"mfc1 $t0, $f0\n"
            assembly_text += f"sw $t0, {variables[varnode.target.id][1]}($fp)\n"
        else:
            assembly_text += f"swc1 $f0, {variables[varnode.target.id][1]}($fp)\n"
    elif left_type == "int" and right_type == "float":
        if (isinstance(node.left, ast.Constant)):
            assembly_text += f"li $t0, {node.left.value}\n"
        else:
            assembly_text += f"lw $t0, {variables[node.left.id][1]}($fp)\n"
        assembly_text += f"mtc1 $t0, $f0\n"
        assembly_text += f"cvt.s.w $f0, $f0\n"



        if (isinstance(node.right, ast.Constant)):
            assembly_text += f"li.s $f1, {node.right.value}\n"
        else:
            assembly_text += f"lwc1 $f1, {variables[node.right.id][1]}($fp)\n"



        if isinstance(node.op, ast.Add):
            assembly_text += f"add.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Sub):
            assembly_text += f"sub.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Mult):
            assembly_text += f"mul.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Div):
            assembly_text += f"div.s $f0, $f0, $f1\n"
        if target_type == "int":
            assembly_text += f"trunc.w.s $f0, $f0\n"
            assembly_text += f"mfc1 $t0, $f0\n"
            assembly_text += f"sw $t0, {variables[varnode.target.id][1]}($fp)\n"
        else:
            assembly_text += f"swc1 $f0, {variables[varnode.target.id][1]}($fp)\n"
    elif left_type == "float" and right_type == "int":
        if (isinstance(node.right, ast.Constant)):
            assembly_text += f"li.s $f0, {node.right.value}\n"
        else:
            assembly_text += f"lwc1 $f0, {variables[node.right.id][1]}($fp)\n"

        
        if (isinstance(node.right, ast.Constant)):
            assembly_text += f"li $t0, {node.right.value}\n"
        else:
            assembly_text += f"lw $t0, {variables[node.right.id][1]}($fp)\n"
        
        assembly_text += f"mtc1 $t0, $f1\n"
        assembly_text += f"cvt.s.w $f1, $f1\n"
        if isinstance(node.op, ast.Add):
            assembly_text += f"add.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Sub):
            assembly_text += f"sub.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Mult):
            assembly_text += f"mul.s $f0, $f0, $f1\n"
        elif isinstance(node.op, ast.Div):
            assembly_text += f"div.s $f0, $f0, $f1\n"
        if target_type == "int":
            assembly_text += f"trunc.w.s $f0, $f0\n"
            assembly_text += f"mfc1 $t0, $f0\n"
            assembly_text += f"sw $t0, {variables[varnode.target.id][1]}($fp)\n"
        else:
            assembly_text += f"swc1 $f0, {variables[varnode.target.id][1]}($fp)\n"

def handle_AnnAssign(node: ast.AnnAssign, variables: dict):
    global assembly_text
    if isinstance(node.value, ast.Constant):
        if variables[node.target.id][0] == "int":
            assembly_text += f"li $t0, {node.value.value}\n"
            assembly_text += f"sw $t0, {variables[node.target.id][1]}($fp)\n"
        elif variables[node.target.id][0] == "float":
            assembly_text += f"li.s $f0, {node.value.value}\n"
            assembly_text += f"swc1 $f0, {variables[node.target.id][1]}($fp)\n"
    elif isinstance(node.value, ast.BinOp):
        handle_binop(node.value, node ,variables)
    elif isinstance(node.value, ast.Name):
        if variables[node.target.id][0] == "int":
            if variables[node.value.id][0] == "int":
                assembly_text += f"lw $t0, {variables[node.value.id][1]}($fp)\n"
                assembly_text += f"sw $t0, {variables[node.target.id][1]}($fp)\n"
            elif variables[node.value.id][0] == "float":
                assembly_text += f"lwc1 $f0, {variables[node.value.id][1]}($fp)\n"
                #convert to int
                assembly_text += f"trunc.w.s $f0, $f0\n"
                assembly_text += f"mfc1 $t0, $f0\n"
                assembly_text += f"sw $t0, {variables[node.target.id][1]}($fp)\n"
        elif variables[node.target.id][0] == "float":
            if variables[node.value.id][0] == "float":
                assembly_text += f"lwc1 $f0, {variables[node.value.id][1]}($fp)\n"
                assembly_text += f"swc1 $f0, {variables[node.target.id][1]}($fp)\n"
            elif variables[node.value.id][0] == "int":
                assembly_text += f"lw $t0, {variables[node.value.id][1]}($fp)\n"
                assembly_text += f"mtc1 $t0, $f0\n"
                assembly_text += f"cvt.s.w $f0, $f0\n"
                assembly_text += f"swc1 $f0, {variables[node.target.id][1]}($fp)\n"
    elif isinstance(node.value, ast.Call):
        if node.value.func.id in std_functions_asm:
            regaddr = 0
            for arg in node.value.args:
                if isinstance(arg, ast.Name):
                    if variables[arg.id][0] == "int":
                        assembly_text += f"lw $a{regaddr}, {variables[arg.id][1]}($fp)\n"
                    elif variables[arg.id][0] == "float":
                        assembly_text += f"lwc1 $f{regaddr + 12}, {variables[arg.id][1]}($fp)\n"
                regaddr += 1
            assembly_text += f"jal {node.value.func.id}\n"
            std_functions.add(node.value.func.id)
        else:
            for arg in node.value.args:
                if isinstance(arg, ast.Name):
                    if variables[arg.id][0] == "int":
                        assembly_text += f"lw $a0, {variables[arg.id][1]}($fp)\n"
                    elif variables[arg.id][0] == "float":
                        assembly_text += f"lwc1 $f12, {variables[arg.id][1]}($fp)\n"
            assembly_text += f"jal {node.value.func.id}\n"
        if (node.annotation.id == "int"):
            assembly_text += f"sw $v0, {variables[node.target.id][1]}($fp)\n"
        elif (node.annotation.id == "float"):
            assembly_text += f"mtc1 $v0, $f0\n"
            assembly_text += f"swc1 $f0, {variables[node.target.id][1]}($fp)\n"

def handle_While(node: ast.While, variables: dict, returnlabel):
    global assembly_text
    global whileloopid
    assembly_text += f"whileloop{whileloopid}:\n"
    handle_Body(node, variables, returnlabel)
    if isinstance(node.test, ast.Compare):
        isFloat = False
        if isinstance(node.test.left, ast.Constant):
            if isinstance(node.test.left.value, float):
                isFloat = True
        elif isinstance(node.test.left, ast.Name):
            if variables[node.test.left.id][0] == "float":
                isFloat = True
        if isinstance(node.test.comparators[0], ast.Constant):
            if isinstance(node.test.comparators[0].value, float):
                isFloat = True
        elif isinstance(node.test.comparators[0], ast.Name):
            if variables[node.test.comparators[0].id][0] == "float":
                isFloat = True
       
        if not isFloat:
            if isinstance(node.test.left, ast.Constant):
                assembly_text += f"li $t0, {node.test.left.value}\n"
            else:
                assembly_text += f"lw $t0, {variables[node.test.left.id][1]}($fp)\n"
            if isinstance(node.test.comparators[0], ast.Constant):
                assembly_text += f"li $t1, {node.test.comparators[0].value}\n"
            else:
                assembly_text += f"lw $t1, {variables[node.test.comparators[0].id][1]}($fp)\n"

            if isinstance(node.test.ops[0], ast.Gt):
                assembly_text += f"bgt $t0, $t1, whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.GtE):
                assembly_text += f"bte $t0, $t1, whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.Lt):
                assembly_text += f"blt $t0, $t1, whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.LtE):
                assembly_text += f"ble $t0, $t1, whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.Eq):
                assembly_text += f"beq $t0, $t1, whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.NotEq):
                assembly_text += f"bne $t0, $t1, whileloop{whileloopid}\n"
        else:
            if isinstance(node.test.left, ast.Constant):
                assembly_text += f"li.s $f0, {node.test.left.value}\n"
            else:
                assembly_text += f"lwc1 $f0, {variables[node.test.left.id][1]}($fp)\n"
            if isinstance(node.test.comparators[0], ast.Constant):
                assembly_text += f"li.s $f1, {node.test.comparators[0].value}\n"
            else:
                assembly_text += f"lwc1 $f1, {variables[node.test.comparators[0].id][1]}($fp)\n"

            
            if isinstance(node.test.ops[0], ast.Gt):
                assembly_text += f"c.le.s $f0, $f1\n"
                assembly_text += f"bc1f whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.GtE):
                assembly_text += f"c.lt.s $f0, $f1\n"
                assembly_text += f"bc1f whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.Lt):
                assembly_text += f"c.lt.s $f0, $f1\n"
                assembly_text += f"bc1t whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.LtE):
                assembly_text += f"c.le.s $f0, $f1\n"
                assembly_text += f"bc1t whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.Eq):
                assembly_text += f"c.eq.s $f0, $f1\n"
                assembly_text += f"bc1t whileloop{whileloopid}\n"
            elif isinstance(node.test.ops[0], ast.NotEq):
                assembly_text += f"c.eq.s $f0, $f1\n"
                assembly_text += f"bc1f whileloop{whileloopid}\n"

    whileloopid += 1

def handle_If(node: ast.If, variables: dict, returnlabel):
    global assembly_text
    global ifstatementId
    if isinstance(node.test, ast.Compare):
        isFloat = False
        if isinstance(node.test.left, ast.Constant):
            if isinstance(node.test.left.value, float):
                isFloat = True
        elif isinstance(node.test.left, ast.Name):
            if variables[node.test.left.id][0] == "float":
                isFloat = True
        if isinstance(node.test.comparators[0], ast.Constant):
            if isinstance(node.test.comparators[0].value, float):
                isFloat = True
        elif isinstance(node.test.comparators[0], ast.Name):
            if variables[node.test.comparators[0].id][0] == "float":
                isFloat = True
        if not isFloat:
            if isinstance(node.test.left, ast.Constant):
                assembly_text += f"li $t0, {node.test.left.value}\n"
            else:
                assembly_text += f"lw $t0, {variables[node.test.left.id][1]}($fp)\n"
            if isinstance(node.test.comparators[0], ast.Constant):
                assembly_text += f"li $t1, {node.test.comparators[0].value}\n"
            else:
                assembly_text += f"lw $t1, {variables[node.test.comparators[0].id][1]}($fp)\n"
            if isinstance(node.test.ops[0], ast.Gt):
                assembly_text += f"ble $t0, $t1, ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.GtE):
                assembly_text += f"blt $t0, $t1, ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.Lt):
                assembly_text += f"bte $t0, $t1, ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.LtE):
                assembly_text += f"bgt $t0, $t1, ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.Eq):
                assembly_text += f"bne $t0, $t1, ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.NotEq):
                assembly_text += f"beq $t0, $t1, ifstmt{ifstatementId}\n"
        else:
            if isinstance(node.test.left, ast.Constant):
                assembly_text += f"li.s $f0, {node.test.left.value}\n"
            else:
                assembly_text += f"lwc1 $f0, {variables[node.test.left.id][1]}($fp)\n"
            if isinstance(node.test.comparators[0], ast.Constant):
                assembly_text += f"li.s $f1, {node.test.comparators[0].value}\n"
            else:
                assembly_text += f"lwc1 $f1, {variables[node.test.comparators[0].id][1]}($fp)\n"

            
            if isinstance(node.test.ops[0], ast.Gt):
                assembly_text += f"c.le.s $f0, $f1\n"
                assembly_text += f"bc1t ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.GtE):
                assembly_text += f"c.lt.s $f0, $f1\n"
                assembly_text += f"bc1t ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.Lt):
                assembly_text += f"c.lt.s $f0, $f1\n"
                assembly_text += f"bc1f ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.LtE):
                assembly_text += f"c.le.s $f0, $f1\n"
                assembly_text += f"bc1f ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.Eq):
                assembly_text += f"c.eq.s $f0, $f1\n"
                assembly_text += f"bc1f ifstmt{ifstatementId}\n"
            elif isinstance(node.test.ops[0], ast.NotEq):
                assembly_text += f"c.eq.s $f0, $f1\n"
                assembly_text += f"bc1t ifstmt{ifstatementId}\n"

        handle_Body(node, variables, returnlabel)

        assembly_text += f"ifstmt{ifstatementId}:\n"
        ifstatementId += 1

def handle_function(node: ast.FunctionDef):
    global assembly_text
    stack_size = 8

    variables = dict()
    returnlabel = f"return{node.name}"

    for arg in node.args.args:
        variables[arg.arg] = arg.annotation.id

    variables.update(allocate_variables(node))

    for name in variables:
        if variables[name] == "int" or variables[name] == "float":
            stack_size += 4
    full_stack_size = stack_size
    #setup function and stack frame
    assembly_text += f"{node.name}:\n"
    assembly_text += f"addi $sp, $sp, -{stack_size} # allocate stack\n"           #allocate stack
    assembly_text += f"sw $fp, {stack_size - 4}($sp) # save old frame pointer\n"  #save old frame pointer
    assembly_text += f"move $fp, $sp # set new frame pointer\n"                   #set new frame pointer
    assembly_text += f"sw $ra, {stack_size - 8}($sp) # save return address\n"    #save return address
    stack_size -= 8
    
    #assign variables to stack
    for name in variables:
        if variables[name] == "int" or variables[name] == "float":
            variables[name] = [variables[name], stack_size - 4]
            stack_size -= 4

    #handle function body
    for index, arg in enumerate(node.args.args):
        var = variables[arg.arg]
        if var[0] == "int":
            assembly_text += f"sw $a{index}, {var[1]}($fp) # store argument {index}\n"
        elif var[0] == "float":
            assembly_text += f"swc1 $f{index + 12}, {var[1]}($fp) # store argument {index}\n"
    
    handle_Body(node,variables, returnlabel)

    #set return variables if they exist
    assembly_text += f"{returnlabel}:\n"

    #clear stack and return
    assembly_text += f"lw $fp, {full_stack_size - 4}($sp) # restore old frame pointer\n" #restore old frame pointer
    assembly_text += f"lw $ra, {full_stack_size - 8}($sp) # restore return address\n" #restore return address
    assembly_text += f"addi $sp, $sp, {full_stack_size} # deallocate stack\n" #deallocate stack
    assembly_text += f"jr $ra # return\n"


def handle_Return(node: ast.Return, variables: dict, returnlabel):
    global assembly_text
    if isinstance(node.value, ast.Constant):
        if isinstance(node.value.value, int):
            assembly_text += f"li $v0, {node.value.value}\n"
        elif isinstance(node.value.value, float):
            assembly_text += f"li.s $f0, {node.value.value}\n"
            assembly_text += f"mfc1 $v0, $f0\n"
    elif isinstance(node.value, ast.Name):
        if variables[node.value.id][0] == "int":
            assembly_text += f"lw $v0, {variables[node.value.id][1]}($fp)\n"
        elif variables[node.value.id][0] == "float":
            assembly_text += f"lwc1 $f0, {variables[node.value.id][1]}($fp)\n"
            assembly_text += f"mfc1 $v0, $f0\n"
    assembly_text += f"j {returnlabel}\n"

def handle_Body(node, variables, returnlabel):
    global assembly_text
    for body_node in node.body:
        if isinstance(body_node, ast.AnnAssign):
            handle_AnnAssign(body_node, variables)
        elif isinstance(body_node, ast.Expr):
            if isinstance(body_node.value, ast.Call):
                if body_node.value.func.id in std_functions_asm:
                    regaddr = 0
                    for arg in body_node.value.args:
                        if isinstance(arg, ast.Name):
                            if variables[arg.id][0] == "int":
                                assembly_text += f"lw $a{regaddr}, {variables[arg.id][1]}($fp)\n"
                            elif variables[arg.id][0] == "float":
                                assembly_text += f"lwc1 $f{regaddr + 12}, {variables[arg.id][1]}($fp)\n"
                        regaddr += 1
                    assembly_text += f"jal {body_node.value.func.id}\n"
                    std_functions.add(body_node.value.func.id)
                else:
                    #TODO: handle function arguments
                    for arg in body_node.value.args:
                        if isinstance(arg, ast.Name):
                            if variables[arg.id][0] == "int":
                                assembly_text += f"lw $a0, {variables[arg.id][1]}($fp)\n"
                            elif variables[arg.id][0] == "float":
                                assembly_text += f"lwc1 $f12, {variables[arg.id][1]}($fp)\n"
                    assembly_text += f"jal {body_node.value.func.id}\n"
        elif isinstance(body_node, ast.While):
            handle_While(body_node, variables, returnlabel)
        elif isinstance(body_node, ast.If):
            handle_If(body_node, variables, returnlabel)
        elif isinstance(body_node, ast.Return):
            handle_Return(body_node, variables, returnlabel)

for node in tree.body:
    if isinstance(node, ast.ImportFrom):
        for name in node.names:
            pass
    elif isinstance(node, ast.FunctionDef):
        handle_function(node)
        pass


# ==================== Generate assembly file ==================== #
assembly_data = ".data\n"
for func in std_functions:
    for line in std_functions_asm[func][0]:
        assembly_data += line + "\n"
assembly_data += "\n.text\n.globl main\n"
for func in std_functions:
    assembly_data += std_functions_asm[func][1] + "\n"
assembly_data += "\n" + assembly_text
#print(assembly_data)
open("source.s", "w").write(assembly_data)