# ============================================================
# Segmento de dados
# ============================================================
.data
str_0: .asciiz "Introduza tamanho e valores: "

# ============================================================
# Segmento de código
# ============================================================
.text
.globl main

main:
    jal f_principal
    li $v0, 10
    syscall

# ---- função media (bastidor = 56 bytes) ----
f_media:
    addiu $sp, $sp, -56
    sw $ra, 52($sp)
    sw $fp, 48($sp)
    addiu $fp, $sp, 56
    lw $t2, 0($fp)
    sw $t2, -56($fp)
    lw $t2, 4($fp)
    sw $t2, -52($fp)
    li $t0, 0
    sw $t0, -48($fp)
    # t1 = int_to_real 0
    li $t0, 0
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -40($fp)
    lw $t0, -40($fp)
    sw $t0, -44($fp)
    li $t0, 0
    sw $t0, -48($fp)
L1:
    # t2 = i < tamanho
    lw $t0, -48($fp)
    lw $t1, -52($fp)
    slt $t2, $t0, $t1
    sw $t2, -36($fp)
    lw $t0, -36($fp)
    beq $t0, $zero, L2
    # t3 = v[i]
    lw $t3, -56($fp)
    lw $t4, -48($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t2, 0($t3)
    sw $t2, -32($fp)
    # t4 = soma + t3
    lw $t0, -44($fp)
    mtc1 $t0, $f0
    lw $t1, -32($fp)
    mtc1 $t1, $f2
    add.s $f4, $f0, $f2
    mfc1 $t0, $f4
    sw $t0, -28($fp)
    lw $t0, -28($fp)
    sw $t0, -44($fp)
    # t5 = i + 1
    lw $t0, -48($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -24($fp)
    lw $t0, -24($fp)
    sw $t0, -48($fp)
    j L1
L2:
    # t6 = int_to_real tamanho
    lw $t0, -52($fp)
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -20($fp)
    # t7 = soma / t6
    lw $t0, -44($fp)
    mtc1 $t0, $f0
    lw $t1, -20($fp)
    mtc1 $t1, $f2
    div.s $f4, $f0, $f2
    mfc1 $t0, $f4
    sw $t0, -16($fp)
    lw $v0, -16($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
f_media_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função principal (bastidor = 440 bytes) ----
f_principal:
    addiu $sp, $sp, -440
    sw $ra, 436($sp)
    sw $fp, 432($sp)
    addiu $fp, $sp, 440
    li $t0, 0
    sw $t0, -440($fp)
    li $t0, 0
    sw $t0, -436($fp)
    # array_zero_init v, 100
    addiu $t3, $fp, -432
    li $t4, 0
    li $t5, 100
_zinit1:
    bge $t4, $t5, _zend2
    sll $t6, $t4, 2
    addu $t7, $t3, $t6
    sw $zero, 0($t7)
    addiu $t4, $t4, 1
    j _zinit1
_zend2:
    # call escrevers, "Introduza tamanho e valores: "
    la $a0, str_0
    li $v0, 4
    syscall
    # t8 = call ler, 0
    li $v0, 5
    syscall
    sw $v0, -32($fp)
    lw $t0, -32($fp)
    sw $t0, -436($fp)
    li $t0, 0
    sw $t0, -440($fp)
L3:
    # t9 = i < n
    lw $t0, -440($fp)
    lw $t1, -436($fp)
    slt $t2, $t0, $t1
    sw $t2, -28($fp)
    lw $t0, -28($fp)
    beq $t0, $zero, L4
    # t10 = call ler, 0
    li $v0, 5
    syscall
    sw $v0, -24($fp)
    # t11 = int_to_real t10
    lw $t0, -24($fp)
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -20($fp)
    # v[i] = t11
    addiu $t3, $fp, -432
    lw $t4, -440($fp)
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    lw $t0, -20($fp)
    sw $t0, 0($t3)
    # t12 = i + 1
    lw $t0, -440($fp)
    li $t1, 1
    addu $t2, $t0, $t1
    sw $t2, -16($fp)
    lw $t0, -16($fp)
    sw $t0, -440($fp)
    j L3
L4:
    # t13 = call media, 2
    addiu $sp, $sp, -8
    addiu $t0, $fp, -432
    sw $t0, 0($sp)
    lw $t0, -436($fp)
    sw $t0, 4($sp)
    jal f_media
    addiu $sp, $sp, 8
    sw $v0, -12($fp)
    # call escrever, t13
    lw $t0, -12($fp)
    mtc1 $t0, $f12
    li $v0, 2
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

