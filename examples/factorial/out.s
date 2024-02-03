.data   
new_line:   .asciiz "\n"
.text   
            .globl  main
terminate:                                              # void -> void
    addi    $sp,                $sp,        -8          # allocate stack
    sw      $fp,                4($sp)                  # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                0($sp)                  # save return address
    li      $v0,                10                      # load immediate argument '10'
    syscall                                             # syscall(10)
    move    $t0,                $v0                     # move return value of syscall to $t0
returnterminate:
    lw      $fp,                4($sp)                  # restore old frame pointer
    lw      $ra,                0($sp)                  # restore return address
    addi    $sp,                $sp,        8           # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


print_newline:                                          # void -> void
    addi    $sp,                $sp,        -8          # allocate stack
    sw      $fp,                4($sp)                  # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                0($sp)                  # save return address
    li      $v0,                4                       # load immediate argument '4'
    la      $a0,                new_line                # load pointer of argument 'new_line'
    syscall                                             # syscall(4, new_line)
    move    $t0,                $v0                     # move return value of syscall to $t0
returnprint_newline:
    lw      $fp,                4($sp)                  # restore old frame pointer
    lw      $ra,                0($sp)                  # restore return address
    addi    $sp,                $sp,        8           # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


print_int:                                              # number: int, new_line: int -> void
    addi    $sp,                $sp,        -20         # allocate stack
    sw      $fp,                16($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                12($sp)                 # save return address
    sw      $a0,                8($fp)                  # store argument number
    sw      $a1,                4($fp)                  # store argument new_line
    li      $v0,                1                       # load immediate argument '1'
    lw      $a0,                8($fp)                  # load argument 'number' from stack
    syscall                                             # syscall(1, number)
    move    $t0,                $v0                     # move return value of syscall to $t0
    li      $t0,                1                       # load immediate value 1
    sw      $t0,                0($fp)                  # save right side of compare to stack: 1
    lw      $t0,                4($fp)                  # load variable new_line from stack
    lw      $t1,                0($fp)                  # load right side of compare from stack: 1
    bne     $t0,                $t1,        iffalse0    # new_line == 1
    jal     print_newline                               # print_newline()
    move    $t0,                $v0                     # move return value of print_newline to $t0
    j       endIf0
iffalse0:   
endIf0:     
returnprint_int:
    lw      $fp,                16($sp)                 # restore old frame pointer
    lw      $ra,                12($sp)                 # restore return address
    addi    $sp,                $sp,        20          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


print_float:                                            # number: float, new_line: int -> void
    addi    $sp,                $sp,        -20         # allocate stack
    sw      $fp,                16($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                12($sp)                 # save return address
    swc1    $f12,               8($fp)                  # store argument number
    sw      $a1,                4($fp)                  # store argument new_line
    li      $v0,                2                       # load immediate argument '2'
    lwc1    $f12,               8($fp)                  # load argument 'number' from stack
    syscall                                             # syscall(2, number)
    move    $t0,                $v0                     # move return value of syscall to $t0
    li      $t0,                1                       # load immediate value 1
    sw      $t0,                0($fp)                  # save right side of compare to stack: 1
    lw      $t0,                4($fp)                  # load variable new_line from stack
    lw      $t1,                0($fp)                  # load right side of compare from stack: 1
    bne     $t0,                $t1,        iffalse1    # new_line == 1
    jal     print_newline                               # print_newline()
    move    $t0,                $v0                     # move return value of print_newline to $t0
    j       endIf1
iffalse1:   
endIf1:     
returnprint_float:
    lw      $fp,                16($sp)                 # restore old frame pointer
    lw      $ra,                12($sp)                 # restore return address
    addi    $sp,                $sp,        20          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


factorial:                                              # n: int -> int
    addi    $sp,                $sp,        -24         # allocate stack
    sw      $fp,                20($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                16($sp)                 # save return address
    sw      $a0,                4($fp)                  # store argument n
    li      $t0,                0                       # load immediate value 0
    sw      $t0,                0($fp)                  # save right side of compare to stack: 0
    lw      $t0,                4($fp)                  # load variable n from stack
    lw      $t1,                0($fp)                  # load right side of compare from stack: 0
    bne     $t0,                $t1,        iffalse2    # n == 0
    li      $t0,                1                       # load immediate value 1
    move    $v0,                $t0                     # return result: return 1
    j       returnfactorial                             # jump to returnfactorial to clean up function
    j       endIf2
iffalse2:   
endIf2:     
    li      $t0,                0                       # load immediate value 0
    sw      $t0,                0($fp)                  # save right side of compare to stack: 0
    lw      $t0,                4($fp)                  # load variable n from stack
    lw      $t1,                0($fp)                  # load right side of compare from stack: 0
    beq     $t0,                $t1,        iffalse3    # n != 0
    lw      $t0,                4($fp)                  # load variable n from stack
    li      $t1,                1                       # load immediate value 1
    sub     $t0,                $t0,        $t1         # n - 1
    sw      $t0,                12($fp)                 # assign next: int = n - 1 in stack
    lw      $a0,                12($fp)                 # load argument 'next' from stack
    jal     factorial                                   # factorial(next)
    move    $t0,                $v0                     # move return value of factorial to $t0
    sw      $t0,                8($fp)                  # assign r: int = factorial(next) in stack
    lw      $t0,                8($fp)                  # load variable r from stack
    lw      $t1,                4($fp)                  # load variable n from stack
    mul     $t0,                $t0,        $t1         # r * n
    mflo    $t0                                         # move integer result of multiplication to $t0
    sw      $t0,                8($fp)                  # assign r: int = r * n in stack
    j       returnfactorial                             # jump to returnfactorial to clean up function
    j       endIf3
iffalse3:   
endIf3:     
returnfactorial:
    lw      $fp,                20($sp)                 # restore old frame pointer
    lw      $ra,                16($sp)                 # restore return address
    addi    $sp,                $sp,        24          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


main:                                                   # void -> void
    addi    $sp,                $sp,        -16         # allocate stack
    sw      $fp,                12($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                8($sp)                  # save return address
    li      $t0,                5                       # load immediate value 5
    sw      $t0,                4($fp)                  # assign n:int = 5 in stack
    lw      $a0,                4($fp)                  # load argument 'n' from stack
    jal     factorial                                   # factorial(n)
    move    $t0,                $v0                     # move return value of factorial to $t0
    sw      $t0,                0($fp)                  # assign f:int = factorial(n) in stack
    lw      $a0,                0($fp)                  # load argument 'f' from stack
    li      $a1,                1                       # load immediate argument '1'
    jal     print_int                                   # print_int(f,1)
    move    $t0,                $v0                     # move return value of print_int to $t0
    jal     print_newline                               # print_newline()
    move    $t0,                $v0                     # move return value of print_newline to $t0
    j       returnmain                                  # jump to returnmain to clean up function
returnmain: 
    lw      $fp,                12($sp)                 # restore old frame pointer
    lw      $ra,                8($sp)                  # restore return address
    addi    $sp,                $sp,        16          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra
