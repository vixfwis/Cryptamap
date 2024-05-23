all.exe: renderer.c
	cl /LD renderer.c
	del renderer.obj
	py main.py
	del renderer.dll
	del renderer.lib
	del renderer.exp