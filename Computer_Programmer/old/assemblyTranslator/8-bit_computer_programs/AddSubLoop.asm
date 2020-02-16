; Simple add loop for the 8-bit computer
; db = Single byte word (Only supported type .. :D)
section .data ; Constant data section
    of db 55d             ; Declare varaible in decimal
    comp db 200d

section .bss ; Modifiable data section
    data1 db 01h           ; Declare varaible in hex
    data2 db 00000010b     ; Declare variable in binary left most bit is MSB

section .text ; Main program section
    main:
        JMP sumLoop
    sumLoop:
        LDA data1
        LDB data2
        SUM
        OUA
        STA
        STB
        LDB of
        SUM
        JC subloop
        JMP sumLoop
    subLoop:
        LDA data1
        LDB data2
        SUB
        OUA
        STA
        STB
        LDB comp
        SUM
        JC subloop
        JMP sumLoop