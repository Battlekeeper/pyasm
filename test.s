.data
avar: .float 23.0
bvar: .float 5.0
cvar: .word 0
strvar: .asciiz "Hello World!"
float_format: .asciiz "%f"
.text
.globl main
print_int:
li $v0, 1
syscall
jr $ra
print_newline:
li   $v0, 11
li   $a0, '\n'
syscall
jr   $ra
terminate:
li   $v0, 10
syscall
main:
l.s $f0, avar
l.s $f1, bvar
sub.s $f2, $f0, $f1
s.s $f2, cvar
cvt.w.s $f2, $f2
mfc1 $t2, $f2
sw $t2, cvar
jal print_newline
lw $a0, cvar
jal print_int
jal terminate
