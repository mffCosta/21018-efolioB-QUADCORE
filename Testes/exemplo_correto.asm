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

# ---- função principal (bastidor = 168 bytes) ----
f_principal:
    addiu $sp, $sp, -168
    sw $ra, 164($sp)
    sw $fp, 160($sp)
    addiu $fp, $sp, 168
    li $t0, 0
    sw $t0, -168($fp)
    li $t0, 0
    sw $t0, -164($fp)
    li $t0, 0x00000000    # 0.0
    sw $t0, -160($fp)
    # array_zero_init vetor, 10
    addiu $t3, $fp, -152
    li $t4, 0
    li $t5, 10
_zinit1:
    bge $t4, $t5, _zend2
    sll $t6, $t4, 2
    addu $t7, $t3, $t6
    sw $zero, 0($t7)
    addiu $t4, $t4, 1
    j _zinit1
_zend2:
    li $t0, 0
    sw $t0, -112($fp)
    li $t0, 0
    sw $t0, -108($fp)
    li $t0, 0
    sw $t0, -104($fp)
    # call escrever, 10
    li $a0, 10
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t1 = call ler, 0
    li $v0, 5
    syscall
    sw $v0, -100($fp)
    lw $t0, -100($fp)
    sw $t0, -164($fp)
    # t2 = call fatorial, 1
    addiu $sp, $sp, -4
    lw $t0, -100($fp)
    sw $t0, 0($sp)
    jal f_fatorial
    addiu $sp, $sp, 4
    sw $v0, -96($fp)
    lw $t0, -96($fp)
    sw $t0, -168($fp)
    # call escrever, resultado
    lw $a0, -168($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t3 = (real) t2
    lw $t0, -96($fp)
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -92($fp)
    lw $t0, -92($fp)
    sw $t0, -160($fp)
    # call escrever, valor_real
    lw $t0, -160($fp)
    mtc1 $t0, $f12
    li $v0, 2
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    li $t0, 0
    sw $t0, -112($fp)
L1:
    # t4 = i < 10
    lw $t0, -112($fp)
    li $t1, 10
    slt $t2, $t0, $t1
    sw $t2, -84($fp)
    lw $t0, -84($fp)
    beq $t0, $zero, L2
    # t5 = i * 2
    lw $t0, -112($fp)
    li $t1, 2
    mul $t2, $t0, $t1
    sw $t2, -80($fp)
    # vetor[i] = t5
    addiu $t3, $fp, -152
    lw $t4, -112($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -80($fp)
    sw $t0, 0($t3)
    # t6 = i + 1
    lw $t0, -112($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -76($fp)
    lw $t0, -76($fp)
    sw $t0, -112($fp)
    j L1
L2:
    li $t0, 0
    sw $t0, -112($fp)
L3:
    # t7 = i < 10
    lw $t0, -112($fp)
    li $t1, 10
    slt $t2, $t0, $t1
    sw $t2, -72($fp)
    lw $t0, -72($fp)
    beq $t0, $zero, L4
    li $t0, 0
    sw $t0, -108($fp)
L5:
    # t8 = j < 9
    lw $t0, -108($fp)
    li $t1, 9
    slt $t2, $t0, $t1
    sw $t2, -68($fp)
    lw $t0, -68($fp)
    beq $t0, $zero, L6
    # t9 = vetor[j]
    addiu $t3, $fp, -152
    lw $t4, -108($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -64($fp)
    # t10 = j + 1
    lw $t0, -108($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -60($fp)
    # t11 = vetor[t10]
    addiu $t3, $fp, -152
    lw $t4, -60($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -56($fp)
    # t12 = t9 > t11
    lw $t0, -64($fp)
    lw $t1, -56($fp)
    sgt $t2, $t0, $t1
    sw $t2, -52($fp)
    lw $t0, -52($fp)
    beq $t0, $zero, L7
    # t13 = vetor[j]
    addiu $t3, $fp, -152
    lw $t4, -108($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -48($fp)
    lw $t0, -48($fp)
    sw $t0, -104($fp)
    # t14 = j + 1
    lw $t0, -108($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -44($fp)
    # t15 = vetor[t14]
    addiu $t3, $fp, -152
    lw $t4, -44($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -40($fp)
    # vetor[j] = t15
    addiu $t3, $fp, -152
    lw $t4, -108($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -40($fp)
    sw $t0, 0($t3)
    # t16 = j + 1
    lw $t0, -108($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -36($fp)
    # vetor[t16] = temp
    addiu $t3, $fp, -152
    lw $t4, -36($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -104($fp)
    sw $t0, 0($t3)
L7:
    # t17 = j + 1
    lw $t0, -108($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -32($fp)
    lw $t0, -32($fp)
    sw $t0, -108($fp)
    j L5
L6:
    # t18 = i + 1
    lw $t0, -112($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -28($fp)
    lw $t0, -28($fp)
    sw $t0, -112($fp)
    j L3
L4:
    li $t0, 0
    sw $t0, -112($fp)
L9:
    # t19 = i < 10
    lw $t0, -112($fp)
    li $t1, 10
    slt $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    beq $t0, $zero, L10
    # t20 = vetor[i]
    addiu $t3, $fp, -152
    lw $t4, -112($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -20($fp)
    # call escrever, t20
    lw $a0, -20($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # t21 = i + 1
    lw $t0, -112($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -16($fp)
    lw $t0, -16($fp)
    sw $t0, -112($fp)
    j L9
L10:
f_principal_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

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
    # t22 = n <= 1
    lw $t0, -32($fp)
    li $t1, 1
    sle $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    beq $t0, $zero, L11
    li $t0, 1
    sw $t0, -28($fp)
    j L12
L11:
    # t23 = n - 1
    lw $t0, -32($fp)
    li $t1, 1
    subu $t2, $t0, $t1
    sw $t2, -20($fp)
    # t24 = call fatorial, 1
    addiu $sp, $sp, -4
    lw $t0, -20($fp)
    sw $t0, 0($sp)
    jal f_fatorial
    addiu $sp, $sp, 4
    sw $v0, -16($fp)
    # t25 = n * t24
    lw $t0, -32($fp)
    lw $t1, -16($fp)
    mul $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $t0, -12($fp)
    sw $t0, -28($fp)
L12:
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

