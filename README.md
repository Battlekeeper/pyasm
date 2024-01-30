# Python like language that compiles to MIPS assembly

### Below is an example program that computes the factorial of 10
[More examples can be found here](https://github.com/Battlekeeper/pyasm/tree/main/examples)

```py
from std_lib import *


# Compute factorial of 50
def main():
    index: int = 1
    total: int = 1

    while index <= 50:
        total: int = total * index
        print_int(total)
        print_newline()
        index: int = 1 + index
    print_newline()
    print_newline()
    print_int(total)
```

### And here is the (no optimisations made) assembly that corresponds to that pyasm program
```asm
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
