#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/priority_queue.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;

typedef unsigned int uint;
typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;

template <typename K, typename V, template <typename> typename Comp = less> using ordered_map = tree<K, V, Comp<K>, rb_tree_tag, tree_order_statistics_node_update>;
template <typename T, template <typename> typename Comp = less> using ordered_set = ordered_map<T, null_type, Comp>;
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
template<typename T> T random(T l, T r) { return uniform_int_distribution<T>(l, r)(rng); }

constexpr int mod = 1'000'000'007;

struct input_data {

    void printTest() {

    }
};

int main() {
    input_data test;
    test.printTest();
    return 0;
}
