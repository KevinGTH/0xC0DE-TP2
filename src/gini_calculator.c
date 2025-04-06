<include stdio.h>

int float_to_int_gini(double gini_float){
    int gini_int = (int)gini_float;
    int result = gini_int + 1;
    return result;
}