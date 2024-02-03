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


harmonic:                                           # n: float -> float
    addi    $sp,            $sp,        -28         # allocate stack
    sw      $fp,            24($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            20($sp)                 # save return address
    swc1    $f12,           4($fp)                  # store argument n
    li.s    $f0,            2.0                     # load immediate value 2.0
    swc1    $f0,            0($fp)                  # save right side of compare to stack: 2.0
    lwc1    $f0,            4($fp)                  # load variable n from stack
    lwc1    $f1,            0($fp)                  # save right side of compare from stack: 2.0
    c.lt.s  $f0,            $f1
    bc1f    iffalse2
    li.s    $f0,            1.0                     # load immediate value 1.0
    mov.s   $f0,            $f0                     # return result: return 1.0
    j       returnharmonic                          # jump to returnharmonic to clean up function
    j       endIf2
iffalse2:   
endIf2:     
    li.s    $f0,            0.0                     # load immediate value 0.0
    swc1    $f0,            0($fp)                  # save right side of compare to stack: 0.0
    lwc1    $f0,            4($fp)                  # load variable n from stack
    lwc1    $f1,            0($fp)                  # save right side of compare from stack: 0.0
    c.eq.s  $f0,            $f1
    bc1t    iffalse3
    lwc1    $f0,            4($fp)                  # load variable n from stack
    li.s    $f1,            1.0                     # load immediate value 1.0
    sub.s   $f0,            $f0,        $f1         # n - 1.0
    swc1    $f0,            16($fp)                 # assign next: float = n - 1.0 in stack
    lwc1    $f12,           16                      # load argument 'next' from stack($fp)
    jal     harmonic                                # harmonic(next)
    move    $t0,            $v0                     # move return value of harmonic to $t0
    swc1    $f0,            12($fp)                 # assign r: float = harmonic(next) in stack
    li.s    $f0,            1.0                     # load immediate value 1.0
    lwc1    $f1,            4($fp)                  # load variable n from stack
    div.s   $f0,            $f0,        $f1         # 1.0 / n
    mflo    $f0                                     # move floating point result of division to $f0
    swc1    $f0,            8($fp)                  # assign div:float = 1.0 / n in stack
    lwc1    $f0,            12($fp)                 # load variable r from stack
    lwc1    $f1,            8($fp)                  # load variable div from stack
    add.s   $f0,            $f0,        $f1         # r + div
    swc1    $f0,            12($fp)                 # assign r: float = r + div in stack
    j       returnharmonic                          # jump to returnharmonic to clean up function
    j       endIf3
iffalse3:   
endIf3:     
returnharmonic:
    lw      $fp,            24($sp)                 # restore old frame pointer
    lw      $ra,            20($sp)                 # restore return address
    addi    $sp,            $sp,        28          # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra


main:                                               # void -> void
    addi    $sp,            $sp,        -16         # allocate stack
    sw      $fp,            12($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            8($sp)                  # save return address
    lwc1    $f0,            4($fp)                  # load variable n from stack
    swc1    $f0,            4($fp)                  # assign n:float = n in stack
    lwc1    $f12,           4                       # load argument 'n' from stack($fp)
    jal     harmonic                                # harmonic(n)
    move    $t0,            $v0                     # move return value of harmonic to $t0
    swc1    $f0,            0($fp)                  # assign h:float = harmonic(n) in stack
    lwc1    $f12,           0                       # load argument 'h' from stack($fp)
    jal     print_float                             # print_float(h)
    move    $t0,            $v0                     # move return value of print_float to $t0
    jal     print_newline                           # print_newline()
    move    $t0,            $v0                     # move return value of print_newline to $t0
returnmain: 
    lw      $fp,            12($sp)                 # restore old frame pointer
    lw      $ra,            8($sp)                  # restore return address
    addi    $sp,            $sp,        16          # deallocate stack
    jr      $ra                                     # return from function by jumping to the pointer in $ra