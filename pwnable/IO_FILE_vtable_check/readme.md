io file vtable check
--------------------
```
Ubuntu 18.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

소스를 보면, 파일을 열고 fp에 저장한 다음, read 함수로 fp 위치에 300바이트만큼 
입력을 받고 있다. 

기본적인 vtable 변조 문제와 비슷하지만, 
우분투 18.04 버전, glibc 2.27 이후 부터는
_IO_vtable_check 함수가 추가되어 참조하는 vtable의 주소가 
_libc_IO_vtables 영역에 존재하는 주소인지를 검증한다. 
따라서 해당 영역에 존재하는 주소를 사용하는 대신 다른 방법을 시도해야 한다. 

_IO_str_jumps 에 _IO_str_overflow 함수를 확인해보면
```
new_buf = (char *) (*((_IO_strfile *) fp)->_s._allocate_buffer) (new_size);
```
위와 같은 루틴이 있는데, 여기서 fp 의 멤버인 _s._allocate_buffer 를 원하는 함수의 주소로 바꾸고, 
new_size 변수를 원하는 인자의 주소로 변경하면 특정 함수를 실행시킬 수 있다. 

_s._allocate_buffer 함수 포인터 호출을 위해선 아래 조건의 만족이 필요하다. 

```
int flush_only = c == EOF;
_IO_size_t pos;
pos = fp->_IO_write_ptr - fp->_IO_write_base;
  if (pos >= (_IO_size_t) (_IO_blen (fp) + flush_only))
```
여기서 IO_write_base를 0으로 만든 다음 IO_write_ptr를 조작하면 
pos를 원하는 값으로 만들 수 있다. 

new_size 변수는 아래 코드에 의해 생성된다. 
```
#define _IO_blen(fp) ((fp)->_IO_buf_end - (fp)->_IO_buf_base)
size_t old_blen = _IO_blen (fp);
_IO_size_t new_size = 2 * old_blen + 100;
if (new_size < old_blen)
   return EOF;
```
요약하면 new_size = 2 ( _IO_buf_end - _IO_buf_base ) +100 인 셈이므로, 
_IO_buf_base 를 0으로 세팅하고 , _IO_buf_end는 (원하는 값 - 100) / 2으로 세팅해야한다. 

이떄, _IO_blen(fp) = _IO_buf_end 가 되므로, 
 if (pos >= (_IO_size_t) (_IO_blen (fp) + flush_only)) 를 만족하려면
 pos >= _IO_buf_end 가 되어야한다. 
 
 따라서 pos = _IO_write_ptr 이므로 _IO_write_ptr = _IO_buf_end 를 만족시켜줘야 한다. 
 즉, _IO_buf_end 와 _IO_write_ptr 모두 (원하는 값 - 100) / 2가 들어가야한다. 
 
이제 문제에 맞춰 입력을 넣어줘보자.

```
const struct _IO_jump_t _IO_file_jumps libio_vtable =
{
  JUMP_INIT_DUMMY,
  JUMP_INIT(finish, _IO_file_finish),
  JUMP_INIT(overflow, _IO_file_overflow),
  JUMP_INIT(underflow, _IO_file_underflow),
  JUMP_INIT(uflow, _IO_default_uflow),
  JUMP_INIT(pbackfail, _IO_default_pbackfail),
  JUMP_INIT(xsputn, _IO_file_xsputn),
  JUMP_INIT(xsgetn, _IO_file_xsgetn),
  JUMP_INIT(seekoff, _IO_new_file_seekoff),
  JUMP_INIT(seekpos, _IO_default_seekpos),
  JUMP_INIT(setbuf, _IO_new_file_setbuf),
  JUMP_INIT(sync, _IO_new_file_sync),
  JUMP_INIT(doallocate, _IO_file_doallocate),
  JUMP_INIT(read, _IO_file_read),
  JUMP_INIT(write, _IO_new_file_write),
  JUMP_INIT(seek, _IO_file_seek),
  JUMP_INIT(close, _IO_file_close),
  JUMP_INIT(stat, _IO_file_stat),
  JUMP_INIT(showmanyc, _IO_default_showmanyc),
  JUMP_INIT(imbue, _IO_default_imbue)
};
```
기존 방식대로면 fclose 내부적으로 실행되는 io_file_finish 를 덮어쓰기 위해
점프테이블 +16 위치에 있는 주소값을 시스템 함수 주소로 변조시켜주었다. 
그러나 지금은 검증루틴으로 인해 그게 불가능하므로, vtable 영역 내의 함수가 되어야한다. 

그래서 finish 함수 주소 자리에 io_str_overflow 의 주소를 넣어주는 것.
우회해서 실행한다고 생각하면 될듯하다.

_IO_str_overflow 의 정상 실행 루틴을 변조시켜야 하고, 그를 위해서는 
덮어줘야 하는건 _IO_write_ptr , _IO_buf_end, _s._allocate_buffer 인데 ,
_IO_str_overflow 를 실행시켜주기 위해서는 _IO_jumps_t 내의 다른 함수를 덮어씌워
해당 함수를 실행하게끔 만들어줘야한다. 

```
p _IO_str_jumps

  __dummy = 0x0, 
  __dummy2 = 0x0, 
  __finish = 0x7fd6aa5d2370 <_IO_str_finish>, 
  __overflow = 0x7fd6aa5d1fd0 <__GI__IO_str_overflow>, 
  __underflow = 0x7fd6aa5d1f70 <__GI__IO_str_underflow>, 
  __uflow = 0x7fd6aa5d0430 <__GI__IO_default_uflow>, 
  __pbackfail = 0x7fd6aa5d2350 <__GI__IO_str_pbackfail>, 
  __xsputn = 0x7fd6aa5d0490 <__GI__IO_default_xsputn>, 
  __xsgetn = 0x7fd6aa5d0640 <__GI__IO_default_xsgetn>, 
  __seekoff = 0x7fd6aa5d24a0 <__GI__IO_str_seekoff>, 
  __seekpos = 0x7fd6aa5d0a00 <_IO_default_seekpos>, 
  __setbuf = 0x7fd6aa5d08d0 <_IO_default_setbuf>, 
  __sync = 0x7fd6aa5d0cc0 <_IO_default_sync>, 
  __doallocate = 0x7fd6aa5d0a70 <__GI__IO_default_doallocate>, 
  __read = 0x7fd6aa5d1e20 <_IO_default_read>, 
  __write = 0x7fd6aa5d1e30 <_IO_default_write>, 
  __seek = 0x7fd6aa5d1e00 <_IO_default_seek>, 
  __close = 0x7fd6aa5d0cc0 <_IO_default_sync>, 
  __stat = 0x7fd6aa5d1e10 <_IO_default_stat>, 
  __showmanyc = 0x7fd6aa5d1e40 <_IO_default_showmanyc>, 
  __imbue = 0x7fd6aa5d1e50 <_IO_default_imbue>
}
```

IO_str_overflow 함수는 str_jump 테이블 + 0x18에 위치한다. 
```
libc 세부 버전에 따라 테이블상 위치가 달라질 수 있음에 유의. 
내 우분투 버전에서는 0x20 위치였지만, 문제에서 주어진 libc 버전에서는 0x8 위치였다. 
```
따라서, IO_finish 자리에는 str_jump+0x20(+0x8) 주소가 들어가게끔 vtable 주소를 세팅해주자.
_IO_finish 는 file_jump + 16 위치에 있으므로,
vtable이 str_overflow-16을 가리켜야 16이 더해져서 해당 함수를 실행한다. 
이 주소들은 libc에 맞게 오프셋 연산을 거쳐야 할듯 . 

fp->_s._allocate_buffer 포인터는 대게 file 구조체에서 vtable 바로 다음에 위치한다. 
해당 위치에 system 함수의 주소를 넣어주면 되겠다. 

정리하면, vtable에는 IO_str_overflow-16 주소값이 들어가야하고 , 
fp->_s._allocate_buffer 에는 system 함수 주소, 
_IO_buf_end 와 _IO_write_ptr 에는 (binsh 주소 - 100) / 2 가 들어가야한다. 
_IO_buf_base 와  IO_write_base 는 0이 들어가면 된다. 

일반적인 경우라면, fp 테이블+ vtable 주소 + fp->_s._allocate_buffer 의 형태로 페이로드를 구성하면 되겠지만 
이 문제는 fp->_s._allocate_buffer 값이 0이 아니면 exit 함수를 호출한다. 

따라서 다른 루틴을 찾아봐야한다. 

```
  0x7f228d0861d0:      mov    rax,QWORD PTR [rbx+0xa0]
=>0x7f228d0861d7:      mov    rcx,QWORD PTR [rax+0x18]
  0x7f228d0861db:      cmp    QWORD PTR [rax+0x20],rcx
  0x7f228d0861df:      jbe    0x7f228d08620d

```

exit 함수 내부 동작을 보자. fp에 대해 동작을 수행중인데 , 
fp 시작주소 + a0 에 있는 포인터를 가져와, 해당 포인터 +0x18값 과 +0x20값을 비교한다. 
해당 루틴을 무시하려면 rax+0x20 의 값이 rcx 값보다 커야한다. 

```
   0x7f11d8e3d1e1:      mov    rax,QWORD PTR [rbx+0xd8]
=> 0x7f11d8e3d1e8:      mov    rdx,rax
   0x7f11d8e3d1eb:      sub    rdx,r13
   0x7f11d8e3d1ee:      cmp    r12,rdx
   0x7f11d8e3d1f1:      jbe    0x7f11d8e3d3a0
   0x7f11d8e3d1f7:      mov    esi,0xffffffff
   0x7f11d8e3d1fc:      mov    rdi,rbx
   0x7f11d8e3d1ff:      call   QWORD PTR [rax+0x18]
```
그 다음으로, fp+0xd8에서 가져온 값이 기준값(libc+0x3e7760)과의 연산에서 
0xd68보다 차가 커야한다. vtable 범위를 넘는 함수를 실행하지 못하게 막고있는것. 

거기까지의 루틴을 통과하면 fp+0xd8에 있는 포인터 + 0x18 을 호출한다. 
따라서, fp+0xd8에서 str_overflow를 호출하게끔 구성을 해보자. 

그러면 exit 함수가 호출됬음에도 불구하고, _IO_str_overflow 루틴으로 들어가게 된다. 
그곳에서 _s._allocate_buffer 함수를 실행시키기 위해 다른 조건들을 맞춰줘 보자 . 

그 다음, ```  if (pos >= (_IO_size_t) (_IO_blen (fp) + flush_only))``` 코드 부분에서
**flush_only가 0이 아닌 1이 들어가므로,** pos에 들어갈 _IO_write_ptr 에 1을 더해서 넣어주어야 한다. 

정리하면, _s._allocate_buffer이 0이 아닐 경우에 exit을 실행시키기 때문에
_IO_str_overflow를 이용한 공격은 불가능해 보이지만, 
exit 내부적으로 IO_finish를 호출하기 때문에 몇가지 조건만 맞춰주면 
_IO_str_overflow를 다시 호출한 공격이 가능하다. 

요약 : exit 함수 내부적으로 에러 발생시에 _IO_finish를 호출할 수 있으니, 
exit() + fp수정 가능시에 이를 이용한 익스플로잇도 된다는 소리

