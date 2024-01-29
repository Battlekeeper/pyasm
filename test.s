.data   
avar:           .word   4
bvar:           .float  3.0
cvar:           .float  0.0
float_format:   .asciiz "%f"

.text   
                .globl  main
print_float:    
    li      $v0,            2
    mov.s   $f12,           $f12
    la      $a0,            float_format
    syscall 
    jr      $ra
terminate:      
    li      $v0,            10
    syscall 
main:           
    lw      $t0,            avar
    l.s     $f1,            bvar
    mtc1    $t0,            $f0
    cvt.s.w $f0,            $f0
    add.s   $f2,            $f0,            $f1
    s.s     $f2,            cvar
    l.s     $f12,           cvar
    jal     print_float
    jal     terminate
