#include <bits/stdc++.h>
using namespace std;

void func();

void solve(istream &cin = std::cin, ostream &cout = std::cout) {

}

signed main() {
    ios_base::sync_with_stdio(false); cin.tie(nullptr);
    int test = 1;
    ifstream cin("../../PROBLEM_NAME/PROBLEM_NAME.in"); // ofstream cout("../../PROBLEM_NAME/PROBLEM_NAME.out");
    cin >> test;
    if (test == 0) cerr << "CHANGE .IN FILE" << endl;
    for (int i = 1; i <= test; i++) {
        const auto divider = string(30, '=');
        cout << divider << ' ' << i << ' ' << divider << '\n';
        solve(cin, cout);
        cout << '\n';
    }
}
