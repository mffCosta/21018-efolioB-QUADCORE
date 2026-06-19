# ============================================================
# Segmento de dados
# ============================================================
.data
g_base: .word 10
g_dobrado: .word 0
g_linha: .word 0
g_tabela: .word 3, 6, 9
__lers_buf: .space 1024

# ============================================================
# Segmento de código
# ============================================================
.text
.globl main

main:
    jal f___init
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
    # t3 = x * 2
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

# ---- função principal (bastidor = 8 bytes) ----
f_principal:
    addiu $sp, $sp, -8
    sw $ra, 4($sp)
    sw $fp, 0($sp)
    addiu $fp, $sp, 8
    # call escrever, base
    lw $a0, g_base
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # call escreverv, tabela
    la $t3, g_tabela
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
    # call escrever, dobrado
    lw $a0, g_dobrado
    li $v0, 1
    syscall
    li $a0, 10
    li $v0, 11
    syscall
    # call escrevers, linha
    lw $t3, g_linha
_puts3:
    lw $a0, 0($t3)
    beq $a0, $zero, _putsend4
    li $v0, 11
    syscall
    addiu $t3, $t3, 4
    j _puts3
_putsend4:
f_principal_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função __init (bastidor = 16 bytes) ----
f___init:
    addiu $sp, $sp, -16
    sw $ra, 12($sp)
    sw $fp, 8($sp)
    addiu $fp, $sp, 16
    # t1 = call dobro, 1
    addiu $sp, $sp, -4
    li $t0, 21
    sw $t0, 0($sp)
    jal f_dobro
    addiu $sp, $sp, 4
    sw $v0, -16($fp)
    lw $t0, -16($fp)
    sw $t0, g_dobrado
    # t2 = call lers, 0
    jal __lers
    sw $v0, -12($fp)
    lw $t0, -12($fp)
    sw $t0, g_linha
f___init_end:
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

