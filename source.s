.data

.text
    .globlmain
print_int:
    li      $v0,            1
    syscall 
    jr      $ra
print_newline:
    li      $v0,            11
    li      $a0,            '\n'
    syscall 
    jr      $ra

main:
    addi    $sp,            $sp,        -16         # allocate stack
    sw      $fp,            12($sp)                 # save old frame pointer
    move    $fp,            $sp                     # set new frame pointer
    sw      $ra,            8($sp)                  # save return address
    li      $t0,            1
    sw      $t0,            4($fp)
    li      $t0,            1
    sw      $t0,            0($fp)
whileloop0:
    lw      $t0,            0($fp)
    lw      $t1,            4($fp)
    mult    $t0,            $t1
    mflo    $t0
    sw      $t0,            0($fp)
    lw      $a0,            0($fp)
    jal     print_int
    jal     print_newline
    li      $t0,            1
    lw      $t1,            4($fp)
    add     $t0,            $t0,        $t1
    sw      $t0,            4($fp)
    lw      $t0,            4($fp)
    li      $t1,            50
    ble     $t0,            $t1,        whileloop0
    jal     print_newline
    jal     print_newline
    lw      $a0,            0($fp)
    jal     print_int
    lw      $fp,            12($sp)                 # restore old frame pointer
    lw      $ra,            8($sp)                  # restore return address
    addi    $sp,            $sp,        16          # deallocate stack
    jr      $ra                                     # return
