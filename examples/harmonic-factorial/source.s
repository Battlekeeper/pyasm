.data   
float_format:   .asciiz "%f"

.text   
                .globl  main
print_newline:  
    li      $v0,                11
    li      $a0,                '\n'
    syscall 
    jr      $ra
print_float:    
    li      $v0,                2
    mov.s   $f12,               $f12
    la      $a0,                float_format
    syscall 
    jr      $ra
print_int:      
    li      $v0,                1
    syscall 
    jr      $ra

factorial:      
    addi    $sp,                $sp,            -20     # allocate stack
    sw      $fp,                16($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                12($sp)                 # save return address
    sw      $a0,                8($fp)                  # store argument 0
    lw      $t0,                8($fp)
    li      $t1,                0
    bne     $t0,                $t1,            ifstmt0
    li      $v0,                1
    j       returnfactorial
ifstmt0:        
    lw      $t0,                8($fp)
    li      $t1,                0
    beq     $t0,                $t1,            ifstmt1
    lw      $t0,                8($fp)
    li      $t1,                1
    sub     $t0,                $t0,            $t1
    sw      $t0,                4($fp)
    lw      $a0,                4($fp)
    jal     factorial
    sw      $v0,                0($fp)
    lw      $t0,                0($fp)
    lw      $t1,                8($fp)
    mult    $t0,                $t1
    mflo    $t0
    sw      $t0,                0($fp)
    lw      $v0,                0($fp)
    j       returnfactorial
ifstmt1:        
returnfactorial:
    lw      $fp,                16($sp)                 # restore old frame pointer
    lw      $ra,                12($sp)                 # restore return address
    addi    $sp,                $sp,            20      # deallocate stack
    jr      $ra                                         # return
harmonic:       
    addi    $sp,                $sp,            -24     # allocate stack
    sw      $fp,                20($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                16($sp)                 # save return address
    swc1    $f12,               12($fp)                 # store argument 0
    lwc1    $f0,                12($fp)
    li.s    $f1,                2.0
    c.lt.s  $f0,                $f1
    bc1f    ifstmt2
    li.s    $f0,                1.0
    mfc1    $v0,                $f0
    j       returnharmonic
ifstmt2:        
    lwc1    $f0,                12($fp)
    li.s    $f1,                0.0
    c.eq.s  $f0,                $f1
    bc1t    ifstmt3
    lwc1    $f0,                12($fp)
    li.s    $f1,                1.0
    sub.s   $f0,                $f0,            $f1
    swc1    $f0,                8($fp)
    lwc1    $f12,               8($fp)
    jal     harmonic
    mtc1    $v0,                $f0
    swc1    $f0,                4($fp)
    li.s    $f0,                1.0
    lwc1    $f1,                12($fp)
    div.s   $f0,                $f0,            $f1
    swc1    $f0,                0($fp)
    lwc1    $f0,                4($fp)
    lwc1    $f1,                0($fp)
    add.s   $f0,                $f0,            $f1
    swc1    $f0,                4($fp)
    lwc1    $f0,                4($fp)
    mfc1    $v0,                $f0
    j       returnharmonic
ifstmt3:        
returnharmonic: 
    lw      $fp,                20($sp)                 # restore old frame pointer
    lw      $ra,                16($sp)                 # restore return address
    addi    $sp,                $sp,            24      # deallocate stack
    jr      $ra                                         # return
main:           
    addi    $sp,                $sp,            -24     # allocate stack
    sw      $fp,                20($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                16($sp)                 # save return address
    li      $t0,                4
    sw      $t0,                12($fp)
    lw      $a0,                12($fp)
    jal     factorial
    sw      $v0,                8($fp)
    lw      $a0,                8($fp)
    jal     print_int
    jal     print_newline
    jal     print_newline
    lw      $a0,                12($fp)
    jal     print_int
    jal     print_newline
    lw      $t0,                12($fp)
    mtc1    $t0,                $f0
    cvt.s.w $f0,                $f0
    swc1    $f0,                4($fp)
    lwc1    $f12,               4($fp)
    jal     harmonic
    mtc1    $v0,                $f0
    swc1    $f0,                0($fp)
    lwc1    $f12,               0($fp)
    jal     print_float
    jal     print_newline
returnmain:     
    lw      $fp,                20($sp)                 # restore old frame pointer
    lw      $ra,                16($sp)                 # restore return address
    addi    $sp,                $sp,            24      # deallocate stack
    jr      $ra                                         # return
