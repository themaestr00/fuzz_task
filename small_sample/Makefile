CC = afl-cc
all: hello.exe
hello.exe: hello.c
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.exe