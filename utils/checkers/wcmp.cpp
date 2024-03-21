#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
    if (argc != 4) {
        std::cout << "ERROR";
        std::cerr << "Usage: " << argv[0] << " <input> <stupid> <smart>" << std::endl;
        return 1;
    }
    std::ifstream stupid(argv[2]);
    if (!stupid.is_open()) {
        std::cout << "ERROR";
        std::cerr << "Error: cannot open " << argv[2] << std::endl;
        return 1;
    }
    std::ifstream smart(argv[3]);
    if (!smart.is_open()) {
        std::cout << "ERROR";
        std::cerr << "Error: cannot open " << argv[3] << std::endl;
        return 1;
    }
    std::string s1, s2;
    int tokenNumber = 0;
    while(stupid >> s1 && smart >> s2) {
        tokenNumber++;
        if (s1 != s2) {
            std::cout << "WA";
            std::cerr << "Error: line " << tokenNumber << ", expected " << s1 << ", found " << s2 << std::endl;
            return 0;
        }
    }
    if (stupid >> s1) {
        std::cout << "WA";
        std::cerr << "Error: line " << tokenNumber + 1 << ", expected " << s1 << ", found nothing" << std::endl;
        return 0;
    }
    if (smart >> s2) {
        std::cout << "WA";
        std::cerr << "Error: line " << tokenNumber + 1 << ", expected nothing, found " << s2 << std::endl;
        return 0;
    }
    std::cout << "OK";
    return 0;
}