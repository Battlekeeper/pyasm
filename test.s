.data
avar: .word 23
bvar: .float 5.0
cvar: .float 0.0
dvar: .float 0.0
float_format: .asciiz "%f"
.text
.globl main
terminate:
li   $v0, 10
syscall
print_newline:
li   $v0, 11
li   $a0, '\n'
syscall
jr   $ra
print_float:
li   $v0, 2
mov.s $f12, $f12
la   $a0, float_format
syscall
jr   $ra
main:
lw $t0, avar
mtc1 $t0, $f0
cvt.s.w $f0, $f0
l.s $f1, bvar
add.s $f2, $f0, $f1
swc1 $f2, cvar
jal print_newline
l.s $f12, cvar
jal print_float
jal print_newline
l.s $f0, cvar
li $t1, 1
mtc1 $t1, $f1
cvt.s.w $f1, $f1
sub.s $f2, $f0, $f1
swc1 $f2, dvar
l.s $f12, dvar
jal print_float
jal terminate
