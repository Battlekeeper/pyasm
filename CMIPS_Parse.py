import ast

variables = dict()
std_functions_asm = dict()
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
                self.data += f"{node.target.id}: .{data_type} {node.value.value}\n"
            else:
                if data_type == "word":
                    self.data += f"{node.target.id}: .{data_type} 0\n"
                elif data_type == "float":
                    self.data += f"{node.target.id}: .{data_type} 0.0\n"
                elif data_type == "asciiz":
                    self.data += f'{node.target.id}: .{data_type} ""\n'

        if isinstance(node.value, ast.BinOp):
            bin_node = node.value
            if isinstance(bin_node.op, ast.Add):
                reg1, reg2 = None, None
                if isinstance(bin_node.left, ast.Constant):
                    if isinstance(bin_node.left.value, int):
                        reg1 = "$t0"
                    else:
                        reg1 = "$f0"
                else:
                    reg1 = "$t0" if variables[bin_node.left.id] == "word" else "$f0"

                if isinstance(bin_node.right, ast.Constant):
                    if isinstance(bin_node.right.value, int):
                        reg2 = "$t1"
                    else:
                        reg2 = "$f1"
                else:
                    reg2 = "$t1" if variables[bin_node.right.id] == "word" else "$f1"

                if isinstance(bin_node.left, ast.Constant):
                    if isinstance(bin_node.left.value, int):
                        self.text += f"li $t0, {bin_node.left.value}\n"
                        if reg2 == "$f1":
                            self.text += f"mtc1 $t0, $f0\n"
                            self.text += f"cvt.s.w $f0, $f0\n"
                            reg1 = "$f0"
                    else:
                        self.text += f"li.s $f0, {bin_node.left.value}\n"
                else:
                    if reg1 == "$t0":
                        if reg2 == "$f1":
                            self.text += f"lw $t0, {bin_node.left.id}\n"
                            self.text += f"mtc1 $t0, $f0\n"
                            self.text += f"cvt.s.w $f0, $f0\n"
                            reg1 = "$f0"
                        else:
                            self.text += f"lw {reg1}, {bin_node.left.id}\n"
                    else:
                        self.text += f"l.s {reg1}, {bin_node.left.id}\n"

                if isinstance(bin_node.right, ast.Constant):
                    if isinstance(bin_node.right.value, int):
                        self.text += f"li $t1, {bin_node.right.value}\n"
                        if reg1 == "$f0":
                            self.text += f"mtc1 $t1, $f1\n"
                            self.text += f"cvt.s.w $f1, $f1\n"
                            reg2 = "$f1"
                    else:
                        self.text += f"li.s $f1, {bin_node.right.value}\n"
                else:
                    if reg2 == "$t1":
                        if reg1 == "$f0":
                            self.text += f"lw $t1, {bin_node.right.id}\n"
                            self.text += f"mtc1 $t1, $f1\n"
                            self.text += f"cvt.s.w $f1, $f1\n"
                            reg2 = "$f1"
                        else:
                            self.text += f"lw {reg2}, {bin_node.right.id}\n"
                    else:
                        self.text += f"l.s {reg2}, {bin_node.right.id}\n"

                # add
                result_reg = "$t2" if variables[node.target.id] == "word" else "$f2"
                if result_reg == "$t2":
                    self.text += f"add {result_reg}, {reg1}, {reg2}\n"
                    self.text += f"sw {result_reg}, {node.target.id}\n"
                else:
                    self.text += f"add.s {result_reg}, {reg1}, {reg2}\n"
                    self.text += f"swc1 {result_reg}, {node.target.id}\n"
            if isinstance(bin_node.op, ast.Sub):
                reg1, reg2 = None, None
                if isinstance(bin_node.left, ast.Constant):
                    if isinstance(bin_node.left.value, int):
                        reg1 = "$t0"
                    else:
                        reg1 = "$f0"
                else:
                    reg1 = "$t0" if variables[bin_node.left.id] == "word" else "$f0"

                if isinstance(bin_node.right, ast.Constant):
                    if isinstance(bin_node.right.value, int):
                        reg2 = "$t1"
                    else:
                        reg2 = "$f1"
                else:
                    reg2 = "$t1" if variables[bin_node.right.id] == "word" else "$f1"

                if isinstance(bin_node.left, ast.Constant):
                    if isinstance(bin_node.left.value, int):
                        self.text += f"li $t0, {bin_node.left.value}\n"
                        if reg2 == "$f1":
                            self.text += f"mtc1 $t0, $f0\n"
                            self.text += f"cvt.s.w $f0, $f0\n"
                            reg1 = "$f0"
                    else:
                        self.text += f"li.s $f0, {bin_node.left.value}\n"
                else:
                    if reg1 == "$t0":
                        if reg2 == "$f1":
                            self.text += f"lw $t0, {bin_node.left.id}\n"
                            self.text += f"mtc1 $t0, $f0\n"
                            self.text += f"cvt.s.w $f0, $f0\n"
                            reg1 = "$f0"
                        else:
                            self.text += f"lw {reg1}, {bin_node.left.id}\n"
                    else:
                        self.text += f"l.s {reg1}, {bin_node.left.id}\n"

                if isinstance(bin_node.right, ast.Constant):
                    if isinstance(bin_node.right.value, int):
                        self.text += f"li $t1, {bin_node.right.value}\n"
                        if reg1 == "$f0":
                            self.text += f"mtc1 $t1, $f1\n"
                            self.text += f"cvt.s.w $f1, $f1\n"
                            reg2 = "$f1"
                    else:
                        self.text += f"li.s $f1, {bin_node.right.value}\n"
                else:
                    if reg2 == "$t1":
                        if reg1 == "$f0":
                            self.text += f"lw $t1, {bin_node.right.id}\n"
                            self.text += f"mtc1 $t1, $f1\n"
                            self.text += f"cvt.s.w $f1, $f1\n"
                            reg2 = "$f1"
                        else:
                            self.text += f"lw {reg2}, {bin_node.right.id}\n"
                    else:
                        self.text += f"l.s {reg2}, {bin_node.right.id}\n"

                # add
                result_reg = "$t2" if variables[node.target.id] == "word" else "$f2"
                if result_reg == "$t2":
                    self.text += f"sub {result_reg}, {reg1}, {reg2}\n"
                    self.text += f"sw {result_reg}, {node.target.id}\n"
                else:
                    self.text += f"sub.s {result_reg}, {reg1}, {reg2}\n"
                    self.text += f"swc1 {result_reg}, {node.target.id}\n"
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
tree = ast.parse(open("source.cmips").read())
# print(ast.dump(tree))
# print(variables)
print()
print(ast.dump(tree))
print()
mips_generator = MIPSGenerator()
mips_assembly = mips_generator.visit(tree, True)
print()
print(variables)
print()
print(mips_assembly)
open("test.s", "w").write(mips_assembly.encode("ascii", "ignore").decode())
