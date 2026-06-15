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
    # t1 = a >= b
    lw $t0, -24($fp)
    lw $t1, -20($fp)
    sge $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    beq $t0, $zero, L1
    lw $t0, -24($fp)
    sw $t0, -16($fp)
    j L2
L1:
    lw $t0, -20($fp)
    sw $t0, -16($fp)
L2:
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
L3:
    # t2 = i < tamanho
    lw $t0, -24($fp)
    lw $t1, -28($fp)
    slt $t2, $t0, $t1
    sw $t2, -20($fp)
    lw $t0, -20($fp)
    beq $t0, $zero, L4
    # t3 = v[i]
    lw $t3, -32($fp)
    lw $t4, -24($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -16($fp)
    # call escrever, t3
    lw $a0, -16($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t4 = i + 1
    lw $t0, -24($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    sw $t0, -24($fp)
    j L3
L4:
f_imprimirVetor_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função principal (bastidor = 112 bytes) ----
f_principal:
    addiu $sp, $sp, -112
    sw $ra, 108($sp)
    sw $fp, 104($sp)
    addiu $fp, $sp, 112
    # array_zero_init numeros, 5
    addiu $t3, $fp, -112
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
    sw $t0, -92($fp)
    li $t0, 0
    sw $t0, -88($fp)
    li $t0, 0
    sw $t0, -84($fp)
    li $t0, 0
    sw $t0, -80($fp)
    li $t0, 0
    sw $t0, -76($fp)
    # numeros[0] = 50
    addiu $t3, $fp, -112
    li $t4, 0
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 50
    sw $t0, 0($t3)
    # numeros[1] = 30
    addiu $t3, $fp, -112
    li $t4, 1
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 30
    sw $t0, 0($t3)
    # numeros[2] = 80
    addiu $t3, $fp, -112
    li $t4, 2
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 80
    sw $t0, 0($t3)
    # numeros[3] = 20
    addiu $t3, $fp, -112
    li $t4, 3
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 20
    sw $t0, 0($t3)
    # numeros[4] = 40
    addiu $t3, $fp, -112
    li $t4, 4
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 40
    sw $t0, 0($t3)
    li $t0, 0
    sw $t0, -92($fp)
L5:
    # t5 = i < 5
    lw $t0, -92($fp)
    li $t1, 5
    slt $t2, $t0, $t1
    sw $t2, -72($fp)
    lw $t0, -72($fp)
    beq $t0, $zero, L6
    # t6 = i + 1
    lw $t0, -92($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -68($fp)
    lw $t0, -68($fp)
    sw $t0, -88($fp)
L7:
    # t7 = j < 5
    lw $t0, -88($fp)
    li $t1, 5
    slt $t2, $t0, $t1
    sw $t2, -64($fp)
    lw $t0, -64($fp)
    beq $t0, $zero, L8
    # t8 = numeros[i]
    addiu $t3, $fp, -112
    lw $t4, -92($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -60($fp)
    # t9 = numeros[j]
    addiu $t3, $fp, -112
    lw $t4, -88($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -56($fp)
    # t10 = t8 > t9
    lw $t0, -60($fp)
    lw $t1, -56($fp)
    sgt $t2, $t0, $t1
    sw $t2, -52($fp)
    lw $t0, -52($fp)
    beq $t0, $zero, L9
    # t11 = numeros[i]
    addiu $t3, $fp, -112
    lw $t4, -92($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -48($fp)
    lw $t0, -48($fp)
    sw $t0, -84($fp)
    # t12 = numeros[j]
    addiu $t3, $fp, -112
    lw $t4, -88($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -44($fp)
    # numeros[i] = t12
    addiu $t3, $fp, -112
    lw $t4, -92($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -44($fp)
    sw $t0, 0($t3)
    # numeros[j] = temp
    addiu $t3, $fp, -112
    lw $t4, -88($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -84($fp)
    sw $t0, 0($t3)
L9:
    # t13 = j + 1
    lw $t0, -88($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -40($fp)
    lw $t0, -40($fp)
    sw $t0, -88($fp)
    j L7
L8:
    # t14 = i + 1
    lw $t0, -92($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -36($fp)
    lw $t0, -36($fp)
    sw $t0, -92($fp)
    j L5
L6:
    # call imprimirVetor, 2
    addiu $sp, $sp, -8
    addiu $t0, $fp, -112
    sw $t0, 0($sp)
    li $t0, 5
    sw $t0, 4($sp)
    jal f_imprimirVetor
    addiu $sp, $sp, 8
    li $t0, 0
    sw $t0, -80($fp)
    li $t0, 0
    sw $t0, -92($fp)
L11:
    # t15 = i < 5
    lw $t0, -92($fp)
    li $t1, 5
    slt $t2, $t0, $t1
    sw $t2, -32($fp)
    lw $t0, -32($fp)
    beq $t0, $zero, L12
    # t16 = numeros[i]
    addiu $t3, $fp, -112
    lw $t4, -92($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -28($fp)
    # t17 = soma + t16
    lw $t0, -80($fp)
    lw $t1, -28($fp)
    addu $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    sw $t0, -80($fp)
    # t18 = i + 1
    lw $t0, -92($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -20($fp)
    lw $t0, -20($fp)
    sw $t0, -92($fp)
    j L11
L12:
    # call escrever, soma
    lw $a0, -80($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t19 = call maximo, 2
    addiu $sp, $sp, -8
    lw $t0, -80($fp)
    sw $t0, 0($sp)
    li $t0, 100
    sw $t0, 4($sp)
    jal f_maximo
    addiu $sp, $sp, 8
    sw $v0, -16($fp)
    lw $t0, -16($fp)
    sw $t0, -76($fp)
    # call escrever, resultado
    lw $a0, -76($fp)
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

