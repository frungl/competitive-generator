#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/priority_queue.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;
namespace r = ranges;
namespace v = views;

typedef unsigned int uint;
typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;

#ifdef LOCAL
#include "debug.h"
#else
#define debug(...) 533
#endif

template <typename K, typename V, template <typename> typename Comp = less> using ordered_map = tree<K, V, Comp<K>, rb_tree_tag, tree_order_statistics_node_update>;
template <typename T, template <typename> typename Comp = less> using ordered_set = ordered_map<T, null_type, Comp>;
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
template<typename T> T random(T l, T r) { return uniform_int_distribution<T>(l, r)(rng); }

constexpr int mod = 1'000'000'007;

void solve(istream &cin = std::cin, ostream &cout = std::cout) {

}
/*

*/
signed main() {
    ios_base::sync_with_stdio(false); cin.tie(nullptr);
    int test = 1;
#if LOCAL
    ifstream cin("../../PROBLEM_NAME/PROBLEM_NAME.in"); // ofstream cout("../../PROBLEM_NAME/PROBLEM_NAME.out");
    cin >> test;
    if (test == 0) cerr << "CHANGE .IN FILE" << endl;
    for (const auto i: v::iota(1) | v::take(test)) {
        const auto divider = string(30, '=');
        cout << divider << ' ' << i << ' ' << divider << '\n';
        solve(cin, cout);
        cout << '\n';
    }
#else
    // ifstream cin(".in"); ofstream cout(".out");
    // cin >> test;
    for (const auto _: v::iota(0, test)) {
        solve(cin, cout);
    }
#endif
}