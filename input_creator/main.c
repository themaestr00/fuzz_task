#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>

enum
{
    MAX_CMD_LINE = 100000
};

int
main(int argc, char *argv[])
{
    char buf[MAX_CMD_LINE] = {};
    int fd = open(argv[1], O_RDONLY);
    int len = read(fd, buf, MAX_CMD_LINE);
    close(fd);
    char *ptr = buf;
    while (*ptr) {
        if (isspace(*ptr)) {
            *ptr = 0;
        }
        ++ptr; 
    }
    fd = open(argv[1], O_WRONLY | O_TRUNC);
    write(fd, buf, len);
    close(fd);
    return 0;
}