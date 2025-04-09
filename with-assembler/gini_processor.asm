section .data
section .bss

section .text
    global asm_process_gini ; Hago visible para el enlazador C

asm_process_gini:
    ; --- Configurar Stack Frame ---
    push ebp          ; Guardar el puntero base anterior
    mov ebp, esp      ; Establecer el nuevo puntero base
    sub esp, 4        ; Reservar 4 bytes en la pila para el entero temporal [ebp-4]

    fld qword [ebp+8]   ; Carga el double de 8 bytes en ST(0)

    fistp dword [ebp-4] ;

    mov eax, [ebp-4]
    inc eax             ; eax = eax + 1
    leave
    ret