    .globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $72, %rsp
    movq -16(%rbp), %rax
    addq $3, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    imulq $5, %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    subq $2, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    addq $1, %rax
    movq %rax, -56(%rbp)
    movq -48(%rbp), %rax
    imulq -56(%rbp), %rax
    movq %rax, -64(%rbp)
    movq -64(%rbp), %rax
    movq %rax, -72(%rbp)
    movq $0, %rax
    leave
    ret
