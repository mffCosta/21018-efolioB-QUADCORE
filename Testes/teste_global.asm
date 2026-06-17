# ============================================================
# Segmento de dados
# ============================================================
.data

# ============================================================
# Segmento de código
# ============================================================
.text
.globl main

main:
    jal f_principal
    li $v0, 10
    syscall

# ---- função fatorial (bastidor = 32 bytes) ----
f_fatorial:
    addiu $sp, $sp, -32
    sw $ra, 28($sp)
    sw $fp, 24($sp)
    addiu $fp, $sp, 32
    lw $t2, 0($fp)
    sw $t2, -32($fp)
    li $t0, 0
    sw $t0, -28($fp)
    # t1 = n <= 1
    lw $t0, -32($fp)
    li $t1, 1
    sle $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    beq $t0, $zero, L1
    li $t0, 1
    sw $t0, -28($fp)
    j L2
L1:
    # t2 = n - 1
    lw $t0, -32($fp)
    li $t1, 1
    subu $t2, $t0, $t1
    sw $t2, -20($fp)
    # t3 = call fatorial, 1
    addiu $sp, $sp, -4
    lw $t0, -20($fp)
    sw $t0, 0($sp)
    jal f_fatorial
    addiu $sp, $sp, 4
    sw $v0, -16($fp)
    # t4 = n * t3
    lw $t0, -32($fp)
    lw $t1, -16($fp)
    mul $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    sw $t0, -28($fp)
L2:
    lw $v0, -28($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
f_fatorial_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função soma (bastidor = 24 bytes) ----
f_soma:
    addiu $sp, $sp, -24
    sw $ra, 20($sp)
    sw $fp, 16($sp)
    addiu $fp, $sp, 24
    lw $t2, 0($fp)
    sw $t2, -24($fp)
    lw $t2, 4($fp)
    sw $t2, -20($fp)
    li $t0, 0
    sw $t0, -16($fp)
    # t5 = a + b
    lw $t0, -24($fp)
    lw $t1, -20($fp)
    addu $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    sw $t0, -16($fp)
    lw $v0, -12($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
f_soma_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função maximo (bastidor = 24 bytes) ----
f_maximo:
    addiu $sp, $sp, -24
    sw $ra, 20($sp)
    sw $fp, 16($sp)
    addiu $fp, $sp, 24
    lw $t2, 0($fp)
    sw $t2, -24($fp)
    lw $t2, 4($fp)
    sw $t2, -20($fp)
    li $t0, 0
    sw $t0, -16($fp)
    # t6 = a >= b
    lw $t0, -24($fp)
    lw $t1, -20($fp)
    sge $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    beq $t0, $zero, L3
    lw $t0, -24($fp)
    sw $t0, -16($fp)
    j L4
L3:
    lw $t0, -20($fp)
    sw $t0, -16($fp)
L4:
    lw $v0, -16($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
f_maximo_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função imprimirVetor (bastidor = 32 bytes) ----
f_imprimirVetor:
    addiu $sp, $sp, -32
    sw $ra, 28($sp)
    sw $fp, 24($sp)
    addiu $fp, $sp, 32
    lw $t2, 0($fp)
    sw $t2, -32($fp)
    lw $t2, 4($fp)
    sw $t2, -28($fp)
    li $t0, 0
    sw $t0, -24($fp)
    li $t0, 0
    sw $t0, -24($fp)
L5:
    # t7 = i < tamanho
    lw $t0, -24($fp)
    lw $t1, -28($fp)
    slt $t2, $t0, $t1
    sw $t2, -20($fp)
    lw $t0, -20($fp)
    beq $t0, $zero, L6
    # t8 = v[i]
    lw $t3, -32($fp)
    lw $t4, -24($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -16($fp)
    # call escrever, t8
    lw $a0, -16($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t9 = i + 1
    lw $t0, -24($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    sw $t0, -24($fp)
    j L5
L6:
f_imprimirVetor_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função principal (bastidor = 128 bytes) ----
f_principal:
    addiu $sp, $sp, -128
    sw $ra, 124($sp)
    sw $fp, 120($sp)
    addiu $fp, $sp, 128
    li $t0, 0
    sw $t0, -128($fp)
    li $t0, 0
    sw $t0, -124($fp)
    li $t0, 0
    sw $t0, -120($fp)
    li $t0, 0
    sw $t0, -116($fp)
    li $t0, 0x00000000    # 0.0
    sw $t0, -112($fp)
    # array_zero_init numeros, 5
    addiu $t3, $fp, -104
    li $t4, 0
    li $t5, 5
_zinit1:
    bge $t4, $t5, _zend2
    sll $t6, $t4, 2
    addu $t7, $t3, $t6
    sw $zero, 0($t7)
    addiu $t4, $t4, 1
    j _zinit1
_zend2:
    li $t0, 0
    sw $t0, -84($fp)
    li $t0, 0
    sw $t0, -80($fp)
    li $t0, 0
    sw $t0, -76($fp)
    li $t0, 0
    sw $t0, -72($fp)
    li $t0, 0
    sw $t0, -68($fp)
    li $t0, 0
    sw $t0, -64($fp)
    li $t0, 5
    sw $t0, -128($fp)
    # t10 = call fatorial, 1
    addiu $sp, $sp, -4
    li $t0, 5
    sw $t0, 0($sp)
    jal f_fatorial
    addiu $sp, $sp, 4
    sw $v0, -60($fp)
    lw $t0, -60($fp)
    sw $t0, -124($fp)
    # call escrever, fat
    lw $a0, -124($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t11 = call soma, 2
    addiu $sp, $sp, -8
    li $t0, 10
    sw $t0, 0($sp)
    li $t0, 20
    sw $t0, 4($sp)
    jal f_soma
    addiu $sp, $sp, 8
    sw $v0, -56($fp)
    lw $t0, -56($fp)
    sw $t0, -120($fp)
    # call escrever, s
    lw $a0, -120($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t12 = call maximo, 2
    addiu $sp, $sp, -8
    lw $t0, -60($fp)
    sw $t0, 0($sp)
    lw $t0, -56($fp)
    sw $t0, 4($sp)
    jal f_maximo
    addiu $sp, $sp, 8
    sw $v0, -52($fp)
    lw $t0, -52($fp)
    sw $t0, -116($fp)
    # call escrever, maior
    lw $a0, -116($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t13 = (real) t12
    lw $t0, -52($fp)
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -48($fp)
    lw $t0, -48($fp)
    sw $t0, -112($fp)
    # call escrever, valorReal
    lw $t0, -112($fp)
    mtc1 $t0, $f12
    li $v0, 2
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # numeros[0] = 50
    addiu $t3, $fp, -104
    li $t4, 0
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 50
    sw $t0, 0($t3)
    # numeros[1] = 30
    addiu $t3, $fp, -104
    li $t4, 1
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 30
    sw $t0, 0($t3)
    # numeros[2] = 80
    addiu $t3, $fp, -104
    li $t4, 2
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 80
    sw $t0, 0($t3)
    # numeros[3] = 20
    addiu $t3, $fp, -104
    li $t4, 3
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 20
    sw $t0, 0($t3)
    # numeros[4] = 40
    addiu $t3, $fp, -104
    li $t4, 4
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 40
    sw $t0, 0($t3)
    # call imprimirVetor, 2
    addiu $sp, $sp, -8
    addiu $t0, $fp, -104
    sw $t0, 0($sp)
    li $t0, 5
    sw $t0, 4($sp)
    jal f_imprimirVetor
    addiu $sp, $sp, 8
    li $t0, 0
    sw $t0, -80($fp)
    li $t0, 0
    sw $t0, -84($fp)
L7:
    # t14 = i < 5
    lw $t0, -84($fp)
    li $t1, 5
    slt $t2, $t0, $t1
    sw $t2, -40($fp)
    lw $t0, -40($fp)
    beq $t0, $zero, L8
    # t15 = numeros[i]
    addiu $t3, $fp, -104
    lw $t4, -84($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -36($fp)
    # t16 = total + t15
    lw $t0, -80($fp)
    lw $t1, -36($fp)
    addu $t2, $t0, $t1
    sw $t2, -32($fp)
    lw $t0, -32($fp)
    sw $t0, -80($fp)
    # t17 = i + 1
    lw $t0, -84($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -28($fp)
    lw $t0, -28($fp)
    sw $t0, -84($fp)
    j L7
L8:
    # call escrever, total
    lw $a0, -80($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t19 = total > 100
    lw $t0, -80($fp)
    li $t1, 100
    sgt $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    beq $t0, $zero, L11
    # t20 = maior > 10
    lw $t0, -116($fp)
    li $t1, 10
    sgt $t2, $t0, $t1
    sw $t2, -20($fp)
    lw $t0, -20($fp)
    beq $t0, $zero, L11
    li $t0, 1
    sw $t0, -16($fp)
    j L12
L11:
    li $t0, 0
    sw $t0, -16($fp)
L12:
    lw $t0, -16($fp)
    beq $t0, $zero, L9
    # call escrever, total
    lw $a0, -80($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    j L10
L9:
    # call escrever, maior
    lw $a0, -116($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
L10:
    li $t0, 14
    sw $t0, -76($fp)
    li $t0, 14
    sw $t0, -72($fp)
    li $t0, 14
    sw $t0, -68($fp)
    li $t0, 0
    sw $t0, -64($fp)
    # call escrever, ot1
    lw $a0, -76($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # call escrever, ot2
    lw $a0, -72($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # call escrever, ot3
    lw $a0, -68($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # call escrever, ot4
    lw $a0, -64($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
f_principal_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

