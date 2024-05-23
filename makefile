renderer.so: renderer.c
	gcc -ggdb -shared -o $@ $^
