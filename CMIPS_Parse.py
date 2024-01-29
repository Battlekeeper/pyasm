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

index = 0


def get_node_register(node, reg_num):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, int):
            return "$t" + str(reg_num)
        elif isinstance(node.value, float):
            return "$f" + str(reg_num)
    elif isinstance(node, ast.Name):
        if variables[node.id] == "word":
            return "$t" + str(reg_num)
        elif variables[node.id] == "float":
            return "$f" + str(reg_num)
def load_node_register(node, reg):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, int):
            return f"li {reg}, {node.value}\n"
        elif isinstance(node.value, float):
            return f"li.s {reg}, {node.value}\n"
    elif isinstance(node, ast.Name):
        if variables[node.id] == "word":
            return f"lw {reg}, {node.id}\n"
        elif variables[node.id] == "float":
            return f"l.s {reg}, {node.id}\n"


class MIPSGenerator(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.assembly = ""
        self.data = ".data\n"
        self.functions = ""
        self.text = ""

    def visit(self, tree, gen_asm=False):
        super().visit(tree)
        if gen_asm:
            for func in std_functions_asm:
                for var in std_functions_asm[func][0]:
                    self.data += var + "\n"
            self.assembly += self.data

            for func in std_functions:
                self.functions += std_functions_asm[func][1] + "\n"


            self.assembly += ".text\n.globl main\n"
            self.assembly += self.functions
            self.assembly += self.text

            return self.assembly

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.text += f"{node.name}:\n"
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        data_type = None
        if node.annotation.id == "int":
            data_type = "word"
        elif node.annotation.id == "float":
            data_type = "float"
        elif node.annotation.id == "str":
            data_type = "asciiz"

        if variables.get(node.target.id) == None:
            variables[node.target.id] = data_type
            if isinstance(node.value, ast.Constant):
                if data_type == "word":
                    self.data += f"{node.target.id}: .word {node.value.value}\n"
                elif data_type == "float":
                    self.data += f"{node.target.id}: .float {node.value.value}\n"
                elif data_type == "asciiz":
                    self.data += f"{node.target.id}: .asciiz \"{node.value.value}\"\n"
            else:
                if data_type == "word":
                    self.data += f"{node.target.id}: .{data_type} 0\n"
                elif data_type == "float":
                    self.data += f"{node.target.id}: .{data_type} 0.0\n"
                elif data_type == "asciiz":
                    self.data += f'{node.target.id}: .{data_type} ""\n'

        if isinstance(node.value, ast.BinOp):
            bin_node = node.value

            
            #TODO refactor to remove duplicate code
            if isinstance(bin_node.op, ast.Add):
                reg0, reg1 = get_node_register(bin_node.left,0), get_node_register(bin_node.right,1)

                self.text += load_node_register(bin_node.left, reg0)
                self.text += load_node_register(bin_node.right, reg1)

                if (reg0.startswith("$t") and reg1.startswith("$t")):
                    self.text += f"add $t2, {reg0}, {reg1}\n"
                    self.text += f"sw $t2, {node.target.id}\n"
                    if (variables[node.target.id] == "float"):
                        self.text += f"mtc1 $t2, $f2\n"
                        self.text += f"cvt.s.w $f2, $f2\n"
                        self.text += f"s.s $f2, {node.target.id}\n"
                elif (reg0.startswith("$f") and reg1.startswith("$f")):
                    self.text += f"add.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
                    if (variables[node.target.id] == "word"):
                        self.text += f"cvt.w.s $f2, $f2\n"
                        self.text += f"mfc1 $t2, $f2\n"
                        self.text += f"sw $t2, {node.target.id}\n"
                elif (reg0[0:2] != reg1[0:1]):
                    if (reg0[0:2] == "$t"):
                        self.text += f"mtc1 $t0, $f0\n"
                        self.text += f"cvt.s.w $f0, $f0\n"
                        reg0 = "$f0"
                    elif (reg1[0:2] == "$f"):
                        self.text += f"mtc1 $t1, $f1\n"
                        self.text += f"cvt.s.w $f1, $f1\n"
                        reg1 = "$f1"
                    self.text += f"add.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
            elif isinstance(bin_node.op, ast.Sub):
                reg0, reg1 = get_node_register(bin_node.left,0), get_node_register(bin_node.right,1)

                self.text += load_node_register(bin_node.left, reg0)
                self.text += load_node_register(bin_node.right, reg1)

                if (reg0.startswith("$t") and reg1.startswith("$t")):
                    self.text += f"sub $t2, {reg0}, {reg1}\n"
                    self.text += f"sw $t2, {node.target.id}\n"
                    if (variables[node.target.id] == "float"):
                        self.text += f"mtc1 $t2, $f2\n"
                        self.text += f"cvt.s.w $f2, $f2\n"
                        self.text += f"s.s $f2, {node.target.id}\n"
                elif (reg0.startswith("$f") and reg1.startswith("$f")):
                    self.text += f"sub.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
                    if (variables[node.target.id] == "word"):
                        self.text += f"cvt.w.s $f2, $f2\n"
                        self.text += f"mfc1 $t2, $f2\n"
                        self.text += f"sw $t2, {node.target.id}\n"
                elif (reg0[0:2] != reg1[0:1]):
                    if (reg0[0:2] == "$t"):
                        self.text += f"mtc1 $t0, $f0\n"
                        self.text += f"cvt.s.w $f0, $f0\n"
                        reg0 = "$f0"
                    elif (reg1[0:2] == "$f"):
                        self.text += f"mtc1 $t1, $f1\n"
                        self.text += f"cvt.s.w $f1, $f1\n"
                        reg1 = "$f1"
                    self.text += f"sub.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
            elif isinstance(bin_node.op, ast.Mult):
                reg0, reg1 = get_node_register(bin_node.left,0), get_node_register(bin_node.right,1)

                self.text += load_node_register(bin_node.left, reg0)
                self.text += load_node_register(bin_node.right, reg1)

                if (reg0.startswith("$t") and reg1.startswith("$t")):
                    self.text += f"mul $t2, {reg0}, {reg1}\n"
                    self.text += f"sw $t2, {node.target.id}\n"
                    if (variables[node.target.id] == "float"):
                        self.text += f"mtc1 $t2, $f2\n"
                        self.text += f"cvt.s.w $f2, $f2\n"
                        self.text += f"s.s $f2, {node.target.id}\n"
                elif (reg0.startswith("$f") and reg1.startswith("$f")):
                    self.text += f"mul.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
                    if (variables[node.target.id] == "word"):
                        self.text += f"cvt.w.s $f2, $f2\n"
                        self.text += f"mfc1 $t2, $f2\n"
                        self.text += f"sw $t2, {node.target.id}\n"
                elif (reg0[0:2] != reg1[0:1]):
                    if (reg0[0:2] == "$t"):
                        self.text += f"mtc1 $t0, $f0\n"
                        self.text += f"cvt.s.w $f0, $f0\n"
                        reg0 = "$f0"
                    elif (reg1[0:2] == "$f"):
                        self.text += f"mtc1 $t1, $f1\n"
                        self.text += f"cvt.s.w $f1, $f1\n"
                        reg1 = "$f1"
                    self.text += f"mul.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
            elif isinstance(bin_node.op, ast.Div):
                reg0, reg1 = get_node_register(bin_node.left,0), get_node_register(bin_node.right,1)

                self.text += load_node_register(bin_node.left, reg0)
                self.text += load_node_register(bin_node.right, reg1)

                if (reg0.startswith("$t") and reg1.startswith("$t")):
                    self.text += f"div $t2, {reg0}, {reg1}\n"
                    self.text += f"mflo $t2\n"
                    self.text += f"sw $t2, {node.target.id}\n"
                    if (variables[node.target.id] == "float"):
                        self.text += f"mtc1 $t2, $f2\n"
                        self.text += f"cvt.s.w $f2, $f2\n"
                        self.text += f"s.s $f2, {node.target.id}\n"
                elif (reg0.startswith("$f") and reg1.startswith("$f")):
                    self.text += f"div.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"
                    if (variables[node.target.id] == "word"):
                        self.text += f"cvt.w.s $f2, $f2\n"
                        self.text += f"mfc1 $t2, $f2\n"
                        self.text += f"sw $t2, {node.target.id}\n"
                elif (reg0[0:2] != reg1[0:1]):
                    if (reg0[0:2] == "$t"):
                        self.text += f"mtc1 $t0, $f0\n"
                        self.text += f"cvt.s.w $f0, $f0\n"
                        reg0 = "$f0"
                    elif (reg1[0:2] == "$f"):
                        self.text += f"mtc1 $t1, $f1\n"
                        self.text += f"cvt.s.w $f1, $f1\n"
                        reg1 = "$f1"
                    self.text += f"div.s $f2, {reg0}, {reg1}\n"
                    self.text += f"s.s $f2, {node.target.id}\n"


        if isinstance(node.value, ast.Name):
            if variables[node.value.id] == "word":
                self.text += f"lw $t0, {node.value.id}\n"
                if (variables[node.target.id] == "float"):
                    self.text += f"mtc1 $t0, $f0\n"
                    self.text += f"cvt.s.w $f0, $f0\n"
                    self.text += f"s.s $f0, {node.target.id}\n"
                else:
                    self.text += f"sw $t0, {node.target.id}\n"
            elif variables[node.value.id] == "float":
                self.text += f"l.s $t0, {node.value.id}\n"
                if (variables[node.target.id] == "float"):
                    self.text += f"cvt.w.s $f0, $f0\n"
                    self.text += f"mfc1 $t0, $f0\n"
                    self.text += f"sw $t0, {node.target.id}\n"
                else:
                    self.text += f"s.s $t0, {node.target.id}\n"
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            std_functions.add(node.value.func.id)
            for arg in node.value.args:
                if isinstance(arg, ast.Constant):
                    if isinstance(arg.value, int):
                        self.text += f"li $a0, {arg.value}\n"
                    elif isinstance(arg.value, float):
                        self.text += f"li.s $f12, {arg.value}\n"
                if isinstance(arg, ast.Name):
                    if variables[arg.id] == "word":
                        self.text += f"lw $a0, {arg.id}\n"
                    elif variables[arg.id] == "float":
                        self.text += f"l.s $f12, {arg.id}\n"
            self.text += f"jal {node.value.func.id}\n"


# Generate MIPS assembly code from AST
tree = ast.parse(open("source.pyasm").read())
print()
print(ast.dump(tree))
print()
mips_generator = MIPSGenerator()
mips_assembly = mips_generator.visit(tree, True)
print(variables)
print()
open("test.s", "w").write(mips_assembly.encode("ascii", "ignore").decode())
