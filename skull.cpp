#include <iostream>
using namespace std;

int main(){
    char alpha[26] = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' };

    string res = "";
    for (int i = 0; i < 10; i++)
        res = res + alpha[rand() % 26];
     
    cout<<res;
}