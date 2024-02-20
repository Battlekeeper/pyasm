main:
    ori     $t0,    $zero,  1
    ori     $t1,    $zero,  1
loop:
    add     $t0,    $t0,    $t1
    j       loop
