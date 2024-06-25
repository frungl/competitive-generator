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

int main(int argc, char *argv[]) {
    if (argc != 4) {
        cout << "ERROR";
        cerr << "Usage: " << argv[0] << " <input> <stupid> <smart>" << endl;
        return 1;
    }
    ifstream input(argv[1]);
    if (!input.is_open()) {
        cout << "ERROR";
        cerr << "Error: cannot open " << argv[1] << endl;
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



    cout << "OK";
    return 0;
}
