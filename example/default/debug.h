#pragma once

#define ANSI_BOLD_RED "\e[1;31m"
#define ANSI_RESET "\e[0m"

namespace cp_debug {
    inline void print(const string &x) {
        cout << '"' << x << '"';
    }

    inline void print(const char *x) {
        cout << '"' << x << '"';
    }

    inline void print(const char &x) {
        cout << '\'' << x << '\'';
    }

    void print(const auto &x) {
        cout << x;
    }

    inline void print(const pair<auto, auto> &x) {
        cout << "{";
        print(x.first);
        cout << ", ";
        print(x.second); cout << "}";
    }

    template <typename T> concept Iterable = requires(T a) { begin(a); end(a); };
    void print(Iterable auto const &x) {
        cout << "{";
        for (int f = 0; auto _val: x) {
            cout << (f++ ? ", " : "");
            print(_val);
        }
        cout << "}";
    }
    void debug_() {
        cout << "]" << ANSI_RESET << '\n';
    }

    void debug_(const auto &t, auto... v) {
        print(t);
        if (sizeof...(v))
            cout << ", ";
        debug_(v...);
    }
}

#define debug(...) cout << ANSI_BOLD_RED << __LINE__ << ": " << "[" << #__VA_ARGS__ << "]" << " = " << "["; cp_debug::debug_(__VA_ARGS__)
