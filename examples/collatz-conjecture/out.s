.data   
new_line:   .asciiz "\n"
.text   
            .globl  main
terminate:                                          # void -> void
    addi    $sp,            $sp,        -8          # allocate stack
    sw      $fp,            4($sp)                  # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            0($sp)                  # save return address
    li      $v0,            10                      # load immediate argument '10'
    syscall                                         # syscall(10)
    move    $t0,            $v0                     # move return value of syscall to $t0
returnterminate:
    lw      $fp,            4($sp)                  # restore old frame pointer
    lw      $ra,            0($sp)                  # restore return address
    addi    $sp,            $sp,        8           # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


print_newline:                                      # void -> void
    addi    $sp,            $sp,        -8          # allocate stack
    sw      $fp,            4($sp)                  # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            0($sp)                  # save return address
    li      $v0,            4                       # load immediate argument '4'
    la      $a0,            new_line                # load pointer of argument 'new_line'
    syscall                                         # syscall(4, new_line)
    move    $t0,            $v0                     # move return value of syscall to $t0
returnprint_newline:
    lw      $fp,            4($sp)                  # restore old frame pointer
    lw      $ra,            0($sp)                  # restore return address
    addi    $sp,            $sp,        8           # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


print_int:                                          # number: int, new_line: int -> void
    addi    $sp,            $sp,        -20         # allocate stack
    sw      $fp,            16($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            12($sp)                 # save return address
    sw      $a0,            8($fp)                  # store argument number
    sw      $a1,            4($fp)                  # store argument new_line
    li      $v0,            1                       # load immediate argument '1'
    lw      $a0,            8($fp)                  # load argument 'number' from stack
    syscall                                         # syscall(1, number)
    move    $t0,            $v0                     # move return value of syscall to $t0
    li      $t0,            1                       # load immediate value 1
    sw      $t0,            0($fp)                  # save right side of compare to stack: 1
    lw      $t0,            4($fp)                  # load variable new_line from stack
    lw      $t1,            0($fp)                  # load right side of compare from stack: 1
    bne     $t0,            $t1,        iffalse0    # new_line == 1
    jal     print_newline                           # print_newline()
    move    $t0,            $v0                     # move return value of print_newline to $t0
    j       endIf0
iffalse0:   
endIf0:     
returnprint_int:
    lw      $fp,            16($sp)                 # restore old frame pointer
    lw      $ra,            12($sp)                 # restore return address
    addi    $sp,            $sp,        20          # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


print_float:                                        # number: float, new_line: int -> void
    addi    $sp,            $sp,        -20         # allocate stack
    sw      $fp,            16($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            12($sp)                 # save return address
    swc1    $f12,           8($fp)                  # store argument number
    sw      $a1,            4($fp)                  # store argument new_line
    li      $v0,            2                       # load immediate argument '2'
    lwc1    $f12,           8($fp)                  # load argument 'number' from stack
    syscall                                         # syscall(2, number)
    move    $t0,            $v0                     # move return value of syscall to $t0
    li      $t0,            1                       # load immediate value 1
    sw      $t0,            0($fp)                  # save right side of compare to stack: 1
    lw      $t0,            4($fp)                  # load variable new_line from stack
    lw      $t1,            0($fp)                  # load right side of compare from stack: 1
    bne     $t0,            $t1,        iffalse1    # new_line == 1
    jal     print_newline                           # print_newline()
    move    $t0,            $v0                     # move return value of print_newline to $t0
    j       endIf1
iffalse1:   
endIf1:     
returnprint_float:
    lw      $fp,            16($sp)                 # restore old frame pointer
    lw      $ra,            12($sp)                 # restore return address
    addi    $sp,            $sp,        20          # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


main:                                               # void -> void
    addi    $sp,            $sp,        -20         # allocate stack
    sw      $fp,            16($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            12($sp)                 # save return address
    li      $t0,            596310                  # load immediate value 596310
    sw      $t0,            8($fp)                  # assign n:int = 596310 in stack
    li      $t0,            0                       # load immediate value 0
    sw      $t0,            4($fp)                  # assign length:int = 0 in stack
startWhile0:
    li      $t0,            1                       # load immediate value 1
    sw      $t0,            0($fp)                  # save right side of compare to stack: 1
    lw      $t0,            8($fp)                  # load variable n from stack
    lw      $t1,            0($fp)                  # load right side of compare from stack: 1
    beq     $t0,            $t1,        endwhile0   # n != 1
    lw      $a0,            8($fp)                  # load argument 'n' from stack
    li      $a1,            1                       # load immediate argument '1'
    jal     print_int                               # print_int(n,1)
    move    $t0,            $v0                     # move return value of print_int to $t0
    li      $t0,            0                       # load immediate value 0
    sw      $t0,            0($fp)                  # save right side of compare to stack: 0
    lw      $t0,            8($fp)                  # load variable n from stack
    li      $t1,            2                       # load immediate value 2
    div     $t0,            $t0,        $t1         # n % 2
    mfhi    $t0                                     # move integer remainder of division to $t0
    lw      $t1,            0($fp)                  # load right side of compare from stack: 0
    bne     $t0,            $t1,        iffalse2    # n % 2 == 0
    lw      $t0,            8($fp)                  # load variable n from stack
    li      $t1,            2                       # load immediate value 2
    div     $t0,            $t0,        $t1         # n / 2
    mflo    $t0                                     # move integer result of division to $t0
    sw      $t0,            8($fp)                  # assign n:int = n / 2 in stack
    j       endIf2
iffalse2:   
    li      $t0,            3                       # load immediate value 3
    lw      $t1,            8($fp)                  # load variable n from stack
    mul     $t0,            $t0,        $t1         # 3 * n
    mflo    $t0                                     # move integer result of multiplication to $t0
    li      $t1,            1                       # load immediate value 1
    add     $t0,            $t0,        $t1         # 3 * n + 1
    sw      $t0,            8($fp)                  # assign n:int = 3 * n + 1 in stack
endIf2:     
    li      $t0,            1                       # load immediate value 1
    lw      $t1,            4($fp)                  # load argument 'length' from stack
    add     $t0,            $t1,        $t0         # length+=1
    sw      $t0,            4($fp)                  # assign length+=1 in stack
    j       startWhile0
endwhile0:  
    li      $a0,            1                       # load immediate argument '1'
    li      $a1,            1                       # load immediate argument '1'
    jal     print_int                               # print_int(1,1)
    move    $t0,            $v0                     # move return value of print_int to $t0
    jal     print_newline                           # print_newline()
    move    $t0,            $v0                     # move return value of print_newline to $t0
    lw      $a0,            4($fp)                  # load argument 'length' from stack
    li      $a1,            1                       # load immediate argument '1'
    jal     print_int                               # print_int(length,1)
    move    $t0,            $v0                     # move return value of print_int to $t0
returnmain: 
    lw      $fp,            16($sp)                 # restore old frame pointer
    lw      $ra,            12($sp)                 # restore return address
    addi    $sp,            $sp,        20          # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


