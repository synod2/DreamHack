oneshot
-------
```
Ubuntu 16.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
```
64비트 바이너리. stdout 주소를 던져주므로 오프셋을 통해 libc 주소를 계산해낼 수 있다. 
입력 가능 바이트는 2E 바이트인데, RBP 까지 덮는데에 0x28바이트가 소모되므로 , 
ret에 덮어쓸수 있는 주소값은 6바이트 뿐이다. 

RBP-8위치에 0을 넣어주는 동작도 필요하므로, 0x18 + 0 + rbp + 원샷가젯 순으로 페이로드를 짜주자. 
6바이트만 덮어쓸 수 있지만, 어차피 리틀엔디안으로 주소값을 보내면 상위 2바이트는 필요가 없다. 

