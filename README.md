# Python like language that compiles to MIPS assembly

### Below is an example program that computes the factorial of 10

```py
from std_lib import *


# Compute factorial of 10
def main():
    index: float = 1.0
    total: float = 1.0

    while index <= 10.0:
        total: float = total * index
        print_float(total)
        print_newline()
        index: float = 1.0 + index
    print_newline()
    print_newline()
    print_float(total)
```

### And here is the (no optimisations made) assembly that corresponds to that pyasm program
```asm
.data   
float_format:   .asciiz "%f"

.text   
                .globl  main
print_newline:  
    li      $v0,            11
    li      $a0,            '\n'
    syscall 
    jr      $ra
print_float:    
    li      $v0,            2
    mov.s   $f12,           $f12
    la      $a0,            float_format
    syscall 
    jr      $ra

main:           
    addi    $sp,            $sp,            -16 # allocate stack
    sw      $fp,            12($sp)             # save old frame pointer
    move    $fp,            $sp                 # set new frame pointer
    sw      $ra,            8($sp)              # save return address
    li.s    $f0,            1.0
    swc1    $f0,            4($fp)
    li.s    $f0,            1.0
    swc1    $f0,            0($fp)
whileloop0:     
    lwc1    $f0,            0($fp)
    lwc1    $f1,            4($fp)
    mul.s   $f0,            $f0,            $f1
    swc1    $f0,            0($fp)
    lwc1    $f12,           0($fp)
    jal     print_float
    jal     print_newline
    li.s    $f0,            1.0
    lwc1    $f1,            4($fp)
    add.s   $f0,            $f0,            $f1
    swc1    $f0,            4($fp)
    lwc1    $f0,            4($fp)
    li.s    $f1,            10.0
    c.le.s  $f0,            $f1
    bc1t    whileloop0
    jal     print_newline
    jal     print_newline
    lwc1    $f12,           0($fp)
    jal     print_float
    lw      $fp,            12($sp)             # restore old frame pointer
    lw      $ra,            8($sp)              # restore return address
    addi    $sp,            $sp,            16  # deallocate stack
    jr      $ra                                 # return
```
