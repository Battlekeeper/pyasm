## Pyasm - It looks like python, low level like C, but feels like Javascript

_so basically its garbage_

### Python like language that compiles to MIPS assembly

### Below is an example program that computes the factorial of 10

[More examples can be found here](https://github.com/Battlekeeper/pyasm/tree/main/examples)

```py
from std_lib import *

def factorial(n: int) -> int:
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)

def main() -> void:
    r:int = factorial(5)
    print_int(r, 1)
```

### And here is the (no optimisations made) assembly that corresponds to that pyasm program

```asm
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
    addi    $sp,                $sp,        -16         # allocate stack
    sw      $fp,                12($sp)                 # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                8($sp)                  # save return address
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
    lw      $t0,                4($fp)                  # load variable n from stack
    li      $t1,                1                       # load immediate value 1
    sub     $t0,                $t0,        $t1         # n - 1
    move    $a0,                $t0                     # move result of 'n - 1' to $a0
    jal     factorial                                   # factorial(n - 1)
    move    $t1,                $v0                     # move result of factorial to $t1
    lw      $t0,                4($fp)                  # load variable n from stack
    mul     $t0,                $t0,        $t1         # n * factorial(n - 1)
    mflo    $t0                                         # move integer result of multiplication to $t0
    move    $v0,                $t0                     # return result: return n * factorial(n - 1)
    j       returnfactorial                             # jump to returnfactorial to clean up function
endIf2:   
returnfactorial:
    lw      $fp,                12($sp)                 # restore old frame pointer
    lw      $ra,                8($sp)                  # restore return address
    addi    $sp,                $sp,        16          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra


main:                                                   # void -> void
    addi    $sp,                $sp,        -12         # allocate stack
    sw      $fp,                8($sp)                  # save old frame pointer
    move    $fp,                $sp                     # set new frame pointer
    sw      $ra,                4($sp)                  # save return address
    li      $a0,                5                       # load immediate argument '5'
    jal     factorial                                   # factorial(5)
    move    $t0,                $v0                     # move return value of factorial to $t0
    sw      $t0,                0($fp)                  # assign r:int = factorial(5) in stack
    lw      $a0,                0($fp)                  # load argument 'r' from stack
    li      $a1,                1                       # load immediate argument '1'
    jal     print_int                                   # print_int(r, 1)
    move    $t0,                $v0                     # move return value of print_int to $t0
returnmain: 
    lw      $fp,                8($sp)                  # restore old frame pointer
    lw      $ra,                4($sp)                  # restore return address
    addi    $sp,                $sp,        12          # deallocate stack
    jr      $ra                                         # return from function by jumping to the pointer in $ra
```

Here is the output of the above assembly as printed to the console

```txt
1
2
6
24
120
720
5040
40320
362880
3628800
39916800
479001600
1932053504
1278945280
2004310016
2004189184
-288522240
-898433024
109641728
-2102132736
-1195114496
-522715136
862453760
-775946240
2076180480
-1853882368
1484783616
-1375731712
-1241513984
1409286144
738197504
-2147483648
-2147483648
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0


0
```
