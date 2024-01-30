.data

.text
.globl main
print_newline:
li   $v0, 11
li   $a0, '\n'
syscall
jr   $ra
print_int:
li $v0, 1
syscall
jr $ra

factorial:
addi $sp, $sp, -20 # allocate stack
sw $fp, 16($sp) # save old frame pointer
move $fp, $sp # set new frame pointer
sw $ra, 12($sp) # save return address
sw $a0, 8($fp) # store argument 0
lw $t0, 8($fp)
li $t1, 0
bne $t0, $t1, ifstmt0
li $v0, 1
j returnfactorial
ifstmt0:
lw $t0, 8($fp)
li $t1, 0
beq $t0, $t1, ifstmt1
lw $t0, 8($fp)
li $t1, 1
sub $t0, $t0, $t1
sw $t0, 4($fp)
lw $a0, 4($fp)
jal factorial
sw $v0, 0($fp)
lw $t0, 0($fp)
lw $t1, 8($fp)
mult $t0, $t1
mflo $t0
sw $t0, 0($fp)
lw $v0, 0($fp)
j returnfactorial
ifstmt1:
returnfactorial:
lw $fp, 16($sp) # restore old frame pointer
lw $ra, 12($sp) # restore return address
addi $sp, $sp, 20 # deallocate stack
jr $ra # return
main:
addi $sp, $sp, -16 # allocate stack
sw $fp, 12($sp) # save old frame pointer
move $fp, $sp # set new frame pointer
sw $ra, 8($sp) # save return address
li $t0, 4
sw $t0, 4($fp)
lw $a0, 4($fp)
jal factorial
sw $v0, 0($fp)
jal print_newline
lw $a0, 0($fp)
jal print_int
returnmain:
lw $fp, 12($sp) # restore old frame pointer
lw $ra, 8($sp) # restore return address
addi $sp, $sp, 16 # deallocate stack
jr $ra # return
