#pragma once

#define ANSI_BOLD_RED "\e[1;31m"
#define ANSI_RESET "\e[0m"

namespace cp_debug {
    inline void print(const string &x) {
        cout << '"' << x << '"';
    }

    inline void print(const string_view &x) {
        cout << '"' << x << '"';
    }

    inline void print(const char *x) {
        cout << '"' << x << '"';
    }

    inline void print(const char &x) {
        cout << '\'' << x << '\'';
    }

    template<typename T>
    void print(const T &x) {
        cout << x;
    }

    template<typename T1, typename T2>
    void print(const pair<T1, T2> &x) {
        cout << "{";
        print(x.first);
        cout << ", ";
        print(x.second); cout << "}";
    }

    template<template<typename> typename K, typename T>
    void print(const K<T> &x) {
        cout << "{";
        int f = 0;
        for (T _val: x) {
            cout << (f++ ? ", " : "");
            print(_val);
        }
        cout << "}";
    }

    void debug_() {
        cout << "]" << ANSI_RESET << '\n';
    }

    template<typename T, typename... V>
    void debug_(const T &t, V &&...v) {
        print(t);
        if (sizeof...(v))
            cout << ", ";
        debug_(v...);
    }
}

#define debug(...) cout << ANSI_BOLD_RED << __LINE__ << ": " << "[" << #__VA_ARGS__ << "]" << " = " << "["; cp_debug::debug_(__VA_ARGS__)
