; Simple add loop for the 8-bit computer
; db = Single byte word (Only supported type .. :D)
section .data ; Constant data section

section .bss ; Modifiable data section
    data1 db 01h           ; Declare varaible in hex
    data2 db 00000010b     ; Declare variable in binary left most bit is MSB

section .text ; Main program section
    main:
        LDA data1
        LDB data2
        JMP sumLoop
    sumLoop:
        SUM
        OUA
        JMP sumLoop