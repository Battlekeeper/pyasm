.data
i: .word 0
float_format: .asciiz "%f"
.text
.globl main
terminate:
li   $v0, 10
syscall
print_int:
li $v0, 1
syscall
jr $ra
main:
lw $a0, i
jal print_int
lw $t0, i
li $t1, 1
add $t2, $t0, $t1
sw $t2, i
jal terminate
