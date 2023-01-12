ORIGIN = $4000
MEMORX = $20
IRQ = $7000
DATA = $6000
DATA2 = $6080
PRINT_VALUE = $3002
ADDS_TO_BUFFER = $3004
PRINT_BUFFER = $3006
CLEAN_BUFFER = $3008

    .ORG ORIGIN
    LDA #$00
    STA $44
    LDY $44

loop:
    LDA DATA, Y
    CMP #$00
    BEQ RESET
    STA ADDS_TO_BUFFER
    JSR ADDNUM
    JMP loop

RESET:
    LDY $44
    LDA #$01
    STA PRINT_BUFFER
    JMP loop

ADDNUM:
    INY
    STY PRINT_VALUE
    RTS

    .ORG DATA
    .DATA "HELLO, WORLD !!!!!"
    .ORG DATA2
    .DATA "NEW STRING !!!!"

    .ORG IRQ
    LDA $44
    STA CLEAN_BUFFER
    ADC #$7F
    STA $44
    LDY $44
    CLI
    JMP loop

; Simulates 6502 inicialization behavior
    .ORG $fffc
    .WORD ORIGIN
    .WORD IRQ

