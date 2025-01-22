#include <stdio.h>
#include <stdlib.h>

int
main(void)
{
    int x, a, b;
    if (scanf("%d%d%d", &x, &a, &b) != 3) {
        return 1;
    }
    if (a <= x && x <= b) {
        printf("Hello world!\n"); // If x is in [a, b] then prints "Hello world!"
    } else {
        abort(); // Else program is terminated with SIGABRT
    }
    return 0;
}