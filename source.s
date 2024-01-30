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

main:
addi $sp, $sp, -32 # allocate stack
sw $fp, 28($sp) # save old frame pointer
move $fp, $sp # set new frame pointer
sw $ra, 24($sp) # save return address
li.s $f0, 7.0
swc1 $f0, 20($fp)
li.s $f0, 2.0
swc1 $f0, 16($fp)
lwc1 $f0, 20($fp)
lwc1 $f1, 16($fp)
div.s $f0, $f0, $f1
swc1 $f0, 12($fp)
li $t0, 0
sw $t0, 8($fp)
lwc1 $f0, 12($fp)
lw $t0, 8($fp)
mtc1 $t0, $f1
cvt.s.w $f1, $f1
add.s $f0, $f0, $f1
trunc.w.s $f0, $f0
mfc1 $t0, $f0
sw $t0, 4($fp)
lw $t0, 4($fp)
li $t1, 3
blt $t0, $t1, ifstmt0
li.s $f0, 69.0
swc1 $f0, 0($fp)
lwc1 $f12, 0($fp)
jal print_float
jal print_newline
ifstmt0:
lwc1 $f12, 12($fp)
jal print_float
jal print_newline
jal terminate
