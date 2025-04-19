#include <stdio.h>

// Declaración de la función externa de Assembler
extern int asm_process_gini(double val);

// Función C que actúa como wrapper (envoltorio)
int float_to_int_gini(double gini_float) {

    // Llamar a la función ensamblador
    int result_from_asm = asm_process_gini(gini_float);
    
    // Devolver el resultado obtenido de ensamblador (que estaba en EAX)
    return result_from_asm;
}

int main() {
    float num = 7.27;
    int num_int = asm_process_gini(num);
    printf("The integer value of %f is %d\n", num, num_int);
    return 0;
}