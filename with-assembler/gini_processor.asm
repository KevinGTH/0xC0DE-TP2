section .data
section .bss

section .text
    global asm_process_gini ; Hago visible para el enlazador C

asm_process_gini:
    ; --- Configurar Stack Frame ---
    push ebp          ; Guardar el puntero base anterior
    mov ebp, esp      ; Establecer el nuevo puntero base
    sub esp, 4        ; Reservar 4 bytes en la pila para el entero temporal [ebp-4]

    fld qword [ebp+8]   ; Cargo el numero flotante pasado por parametro en el tope de la pila

    fistp dword [ebp-4] ;Saco el valor tope de la pila convirtiendolo  a entero en la MEMORIA

    mov eax, [ebp-4]
    inc eax             ; eax = eax + 1
    leave       ;esto reemplaza las instrucciones: 1)mov esp,ebp 2)pop ebp
    ret