# ============================================================
# Segmento de dados
# ============================================================
.data
g_g: .word 7
g_gr: .float 1.5
__lers_buf: .space 1024

# ============================================================
# Segmento de código
# ============================================================
.text
.globl main

main:
    jal f_principal
    li $v0, 10
    syscall

# ---- função dobro (bastidor = 16 bytes) ----
f_dobro:
    addiu $sp, $sp, -16
    sw $ra, 12($sp)
    sw $fp, 8($sp)
    addiu $fp, $sp, 16
    lw $t2, 0($fp)
    sw $t2, -16($fp)
    # t1 = x * 2
    lw $t0, -16($fp)
    li $t1, 2
    mul $t2, $t0, $t1
    sw $t2, -12($fp)
    lw $v0, -12($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
f_dobro_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função principal (bastidor = 152 bytes) ----
f_principal:
    addiu $sp, $sp, -152
    sw $ra, 148($sp)
    sw $fp, 144($sp)
    addiu $fp, $sp, 152
    li $t0, 1
    sw $t0, -152($fp)
    li $t0, 2
    sw $t0, -148($fp)
    li $t0, 3
    sw $t0, -144($fp)
    li $t0, 0x4048F5C3    # 3.14
    sw $t0, -140($fp)
    # t4 = int_to_real 2
    li $t0, 2
    mtc1 $t0, $f0
    cvt.s.w $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -128($fp)
    # t5 = 3.14 / t4
    li $t0, 0x4048F5C3    # 3.14
    mtc1 $t0, $f0
    lw $t1, -128($fp)
    mtc1 $t1, $f2
    div.s $f4, $f0, $f2
    mfc1 $t0, $f4
    sw $t0, -124($fp)
    lw $t0, -124($fp)
    sw $t0, -132($fp)
    # v[0] = 10
    addiu $t3, $fp, -120
    li $t4, 0
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 10
    sw $t0, 0($t3)
    # v[1] = 20
    addiu $t3, $fp, -120
    li $t4, 1
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 20
    sw $t0, 0($t3)
    # v[2] = 30
    addiu $t3, $fp, -120
    li $t4, 2
    sll $t4, $t4, 2
    addu $t3, $t3, $t4
    li $t0, 30
    sw $t0, 0($t3)
    # t6 = call lers, 0
    jal __lers
    sw $v0, -100($fp)
    lw $t0, -100($fp)
    sw $t0, -108($fp)
    li $v0, 12
    syscall
    sw $v0, -92($fp)
    lw $t0, -92($fp)
    sw $t0, -96($fp)
    li $t0, 3
    sw $t0, -88($fp)
    li $t0, 2
    sw $t0, -84($fp)
    # t10 = -m
    lw $t0, -152($fp)
    subu $t2, $zero, $t0
    sw $t2, -76($fp)
    lw $t0, -76($fp)
    sw $t0, -80($fp)
    # t11 = (inteiro) x
    lw $t0, -140($fp)
    mtc1 $t0, $f0
    trunc.w.s $f0, $f0
    mfc1 $t0, $f0
    sw $t0, -68($fp)
    lw $t0, -68($fp)
    sw $t0, -72($fp)
    # t13 = m > 0
    lw $t0, -152($fp)
    li $t1, 0
    sgt $t2, $t0, $t1
    sw $t2, -60($fp)
    lw $t0, -60($fp)
    bne $t0, $zero, L3
    # t14 = n < 0
    lw $t0, -148($fp)
    li $t1, 0
    slt $t2, $t0, $t1
    sw $t2, -56($fp)
    lw $t0, -56($fp)
    bne $t0, $zero, L3
    li $t0, 0
    sw $t0, -52($fp)
    j L4
L3:
    li $t0, 1
    sw $t0, -52($fp)
L4:
    lw $t0, -52($fp)
    beq $t0, $zero, L1
    # call escrever, m
    lw $a0, -152($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
L1:
    # t15 = m > 5
    lw $t0, -152($fp)
    li $t1, 5
    sgt $t2, $t0, $t1
    sw $t2, -48($fp)
    # t16 = t15 == 0
    lw $t0, -48($fp)
    li $t1, 0
    seq $t2, $t0, $t1
    sw $t2, -44($fp)
    lw $t0, -44($fp)
    beq $t0, $zero, L5
    # call escrever, n
    lw $a0, -148($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
L5:
    # t19 = m > 0
    lw $t0, -152($fp)
    li $t1, 0
    sgt $t2, $t0, $t1
    sw $t2, -40($fp)
    lw $t0, -40($fp)
    beq $t0, $zero, L11
    # t20 = n > 0
    lw $t0, -148($fp)
    li $t1, 0
    sgt $t2, $t0, $t1
    sw $t2, -36($fp)
    lw $t0, -36($fp)
    beq $t0, $zero, L11
    li $t0, 1
    sw $t0, -32($fp)
    j L12
L11:
    li $t0, 0
    sw $t0, -32($fp)
L12:
    lw $t0, -32($fp)
    bne $t0, $zero, L9
    # t21 = soma > 100
    lw $t0, -144($fp)
    li $t1, 100
    sgt $t2, $t0, $t1
    sw $t2, -28($fp)
    lw $t0, -28($fp)
    bne $t0, $zero, L9
    li $t0, 0
    sw $t0, -24($fp)
    j L10
L9:
    li $t0, 1
    sw $t0, -24($fp)
L10:
    lw $t0, -24($fp)
    beq $t0, $zero, L7
    # call escrever, soma
    lw $a0, -144($fp)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
L7:
    # call escreverc, c
    lw $a0, -96($fp)
    li $v0, 11
    syscall
    # call escreverv, v
    addiu $t3, $fp, -120
    li $t5, 3
_pv1:
    blez $t5, _pvend2
    lw $a0, 0($t3)
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    addiu $t3, $t3, 4
    addiu $t5, $t5, -1
    j _pv1
_pvend2:
    # call escrevers, s
    lw $t3, -108($fp)
_puts3:
    lw $a0, 0($t3)
    beq $a0, $zero, _putsend4
    li $v0, 11
    syscall
    addiu $t3, $t3, 4
    j _puts3
_putsend4:
    # t22 = g > 0
    lw $t0, g_g
    li $t1, 0
    sgt $t2, $t0, $t1
    sw $t2, -20($fp)
    lw $t0, -20($fp)
    beq $t0, $zero, L13
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
L13:
    # t23 = call dobro, 1
    addiu $sp, $sp, -4
    lw $t0, g_g
    sw $t0, 0($sp)
    jal f_dobro
    addiu $sp, $sp, 4
    sw $v0, -16($fp)
    # call escrever, t23
    lw $a0, -16($fp)
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

# ---- runtime: lers (lê uma linha como inteiro[] terminado em 0) ----
__lers:
    la $a0, __lers_buf
    li $a1, 1024
    li $v0, 8
    syscall
    li $v0, 9
    li $a0, 1024
    syscall
    move $t0, $v0
    move $t1, $v0
    la $t2, __lers_buf
__lers_loop:
    lb $t4, 0($t2)
    beq $t4, $zero, __lers_done
    li $t5, 10
    beq $t4, $t5, __lers_done
    sw $t4, 0($t1)
    addiu $t1, $t1, 4
    addiu $t2, $t2, 1
    j __lers_loop
__lers_done:
    sw $zero, 0($t1)
    move $v0, $t0
    jr $ra

