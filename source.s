.data   
float_format:   .asciiz "%f"

.text   
                .globl  main
print_float:    
    li      $v0,            2
    mov.s   $f12,           $f12
    la      $a0,            float_format
    syscall 
    jr      $ra
print_newline:  
    li      $v0,            11
    li      $a0,            '\n'
    syscall 
    jr      $ra

main:           
    addi    $sp,            $sp,            -20 # allocate stack
    sw      $fp,            16($sp)             # save old frame pointer
    move    $fp,            $sp                 # set new frame pointer
    sw      $ra,            12($sp)             # save return address
    li.s    $f0,            1.0
    swc1    $f0,            8($fp)
    li.s    $f0,            1.0
    swc1    $f0,            4($fp)
whileloop0:     
    lwc1    $f0,            4($fp)
    lwc1    $f1,            8($fp)
    mul.s   $f0,            $f0,            $f1
    swc1    $f0,            4($fp)
    lwc1    $f12,           4($fp)
    jal     print_float
    jal     print_newline
    li.s    $f0,            1.0
    swc1    $f0,            0($fp)
    lwc1    $f0,            8($fp)
    lwc1    $f1,            0($fp)
    add.s   $f0,            $f0,            $f1
    swc1    $f0,            8($fp)
    lwc1    $f0,            8($fp)
    li.s    $f1,            10.0
    c.le.s  $f0,            $f1
    bc1t    whileloop0
    jal     print_newline
    jal     print_newline
    lwc1    $f12,           4($fp)
    jal     print_float
    lw      $fp,            16($sp)             # restore old frame pointer
    lw      $ra,            12($sp)             # restore return address
    addi    $sp,            $sp,            20  # deallocate stack
    jr      $ra                                 # return
