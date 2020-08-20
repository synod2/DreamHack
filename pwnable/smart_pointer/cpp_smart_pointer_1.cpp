// g++ -o pwn-smart-poiner-1 pwn-smart-pointer-1.cpp -no-pie -std=c++11

#include <iostream>
#include <memory>
#include <csignal>
#include <unistd.h>
#include <cstdio>
#include <cstring>
#include <cstdio>
#include <cstdlib>

char* guest_book = "guestbook\x00";

void alarm_handler(int trash)
{
    std::cout << "TIME OUT" << std::endl;
    exit(-1);
}

void initialize()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGALRM, alarm_handler);
    alarm(30);
}

void print_menu(){
    std::cout << "smart pointer system!" << std::endl;
    std::cout << "1. change smart pointer" << std::endl;
    std::cout << "2. delete smart pointer" << std::endl;
    std::cout << "3. test smart pointer" << std::endl;
    std::cout << "4. write guest book" << std::endl;
    std::cout << "5. view guest book" << std::endl;
    std::cout << "6. exit system" << std::endl;
    std::cout << "[*] select : ";
}

void write_guestbook(){
    std::string data;
    std::cout << "write guestbook : ";
    std::cin >> data;
    guest_book = (char *)malloc(data.length() + 1);
    strcpy(guest_book, data.c_str());
}

void view_guestbook(){
    std::cout << "guestbook data: ";
    std::cout << guest_book << std::endl;
}

void apple(){
    std::cout << "Hi im apple!" << std::endl;
}

void banana(){
    std::cout << "Hi im banana!" << std::endl;
}

void mango(){
    std::cout << "Hi im mango!" << std::endl;
}

void getshell(){
    std::cout << "Hi im shell!" << std::endl;
    std::cout << "what? shell?" << std::endl;
    system("/bin/sh");
}

class Smart{
public:
    Smart(){
        fp = apple;
    }
    Smart(const Smart&){
    }

    void change_function(int select){
        if(select == 1){
            fp = apple;
        } else if(select == 2){
            fp = banana;
        } else if(select == 3){
            fp = mango;
        } else {
            fp = apple;
        }
    }
    void (*fp)(void);
};

void change_pointer(std::shared_ptr<Smart> first){
    int selector = 0;
    std::cout << "1. apple\n2. banana\n3. mango" << std::endl;
    std::cout << "select function for smart pointer: ";
    std::cin >> selector;
    (*first).change_function(selector);
    std::cout << std::endl;
}

int main(){
    initialize();
    int selector = 0;
    Smart *smart = new Smart();
    std::shared_ptr<Smart> src_ptr(smart);
    std::shared_ptr<Smart> new_ptr(smart);
    while(1){
        print_menu();
        std::cin >> selector;
        switch(selector){
            case 1:
                std::cout << "Select pointer(1, 2): ";
                std::cin >> selector;
                if(selector == 1){
                    change_pointer(src_ptr);
                } else if(selector == 2){
                    change_pointer(new_ptr);
                }
                break;
            case 2:
                std::cout << "Select pointer(1, 2): ";
                std::cin >> selector;
                if(selector == 1){
                    src_ptr.reset();
                } else if(selector == 2){
                    new_ptr.reset();
                }
                break;
            case 3:
                std::cout << "Select pointer(1, 2): ";
                std::cin >> selector;
                if(selector == 1){
                    (*src_ptr).fp();
                } else if(selector == 2){
                    (*new_ptr).fp();
                }
                break;
            case 4:
                write_guestbook();
                break;
            case 5:
                view_guestbook();
                break;
            case 6:
                return 0;
                break;
            default:
                break;
        }
    }
}