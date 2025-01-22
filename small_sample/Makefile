CC = /usr/local/bin/afl-gcc
CFLAGS = -Werror -Wall
all: hello.exe
hello.exe: hello.c
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.exe