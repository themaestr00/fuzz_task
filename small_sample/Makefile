CC = /usr/local/bin/afl-gcc
all: hello.exe
hello.exe: hello.c
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.exe