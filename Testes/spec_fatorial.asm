# ============================================================
# Segmento de dados
# ============================================================
.data
str_0: .asciiz "Introduza inteiro: "

# ============================================================
# Segmento de código
# ============================================================
.text
.globl main

main:
    jal f_principal
    li $v0, 10
    syscall

# ---- função fact (bastidor = 32 bytes) ----
f_fact:
    addiu $sp, $sp, -32
    sw $ra, 28($sp)
    sw $fp, 24($sp)
    addiu $fp, $sp, 32
    lw $t2, 0($fp)
    sw $t2, -32($fp)
    # t1 = k <= 1
    lw $t0, -32($fp)
    li $t1, 1
    sle $t2, $t0, $t1
    sw $t2, -28($fp)
    lw $t0, -28($fp)
    beq $t0, $zero, L1
    li $v0, 1
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
    j L2
L1:
    # t2 = k - 1
    lw $t0, -32($fp)
    li $t1, 1
    subu $t2, $t0, $t1
    sw $t2, -24($fp)
    # t3 = call fact, 1
    addiu $sp, $sp, -4
    lw $t0, -24($fp)
    sw $t0, 0($sp)
    jal f_fact
    addiu $sp, $sp, 4
    sw $v0, -20($fp)
    # t4 = k * t3
    lw $t0, -32($fp)
    lw $t1, -20($fp)
    mul $t2, $t0, $t1
    sw $t2, -16($fp)
    lw $v0, -16($fp)
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra
L2:
f_fact_end:
    lw $ra, -4($fp)
    lw $t8, -8($fp)
    move $sp, $fp
    move $fp, $t8
    jr $ra

# ---- função principal (bastidor = 24 bytes) ----
f_principal:
    addiu $sp, $sp, -24
    sw $ra, 20($sp)
    sw $fp, 16($sp)
    addiu $fp, $sp, 24
    li $t0, 0
    sw $t0, -24($fp)
    # call escrevers, "Introduza inteiro: "
    la $a0, str_0
    li $v0, 4
    syscall
    # t5 = call ler, 0
    li $v0, 5
    syscall
    sw $v0, -20($fp)
    lw $t0, -20($fp)
    sw $t0, -24($fp)
    # t6 = call fact, 1
    addiu $sp, $sp, -4
    lw $t0, -20($fp)
    sw $t0, 0($sp)
    jal f_fact
    addiu $sp, $sp, 4
    sw $v0, -16($fp)
    # call escrever, t6
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

