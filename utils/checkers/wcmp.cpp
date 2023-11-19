#include <bits/stdc++.h>
using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 4) {
        cout << "ERROR";
        cerr << "Usage: " << argv[0] << " <input> <stupid> <smart>" << endl;
        return 1;
    }
    ifstream stupid(argv[2]);
    if (!stupid.is_open()) {
        cout << "ERROR";
        cerr << "Error: cannot open " << argv[2] << endl;
        return 1;
    }
    ifstream smart(argv[3]);
    if (!smart.is_open()) {
        cout << "ERROR";
        cerr << "Error: cannot open " << argv[3] << endl;
        return 1;
    }
    string s1, s2;
    int tokenNumber = 0;
    while(stupid >> s1 && smart >> s2) {
        tokenNumber++;
        if (s1 != s2) {
            cout << "WA";
            cerr << "Error: line " << tokenNumber << ", expected " << s1 << ", found " << s2 << endl;
            return 0;
        }
    }
    if (stupid >> s1) {
        cout << "WA";
        cerr << "Error: line " << tokenNumber + 1 << ", expected " << s1 << ", found nothing" << endl;
        return 0;
    }
    if (smart >> s2) {
        cout << "WA";
        cerr << "Error: line " << tokenNumber + 1 << ", expected nothing, found " << s2 << endl;
        return 0;
    }
    cout << "OK";
    return 0;
}