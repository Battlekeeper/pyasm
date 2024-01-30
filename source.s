.data
float_format: .asciiz "%f"

.text
.globl main
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
terminate:
li   $v0, 10
syscall
print_int:
li $v0, 1
syscall
jr $ra

main:
addi $sp, $sp, -24 # allocate stack
sw $fp, 20($sp) # save old frame pointer
move $fp, $sp # set new frame pointer
sw $ra, 16($sp) # save return address
li.s $f0, 7.0
swc1 $f0, 12($fp)
li.s $f0, 2.0
swc1 $f0, 8($fp)
lwc1 $f0, 12($fp)
lwc1 $f1, 8($fp)
div.s $f0, $f0, $f1
swc1 $f0, 4($fp)
lwc1 $f0, 4($fp)
trunc.w.s $f0, $f0
mfc1 $t0, $f0
sw $t0, 0($fp)
lw $a0, 0($fp)
jal print_int
jal print_newline
lwc1 $f12, 4($fp)
jal print_float
jal terminate
