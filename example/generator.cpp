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
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;

void print_(const string &x) { cerr << '"' << x << '"'; }
void print_(const auto &x) { cerr << x; }
void print_(const pair<auto, auto> &x) { cerr << "{"; print_(x.first); cerr << ", "; print_(x.second); cerr << "}"; }
template <typename T> concept Iterable = requires(T a) { begin(a); end(a); };
void print_(Iterable auto const &x) { cerr << "{"; for (int f = 0; auto _val : x) { cerr << (f++ ? ", " : ""); print_(_val); } cerr << "}"; }
void debug_() { cerr << "]\n"; }
void debug_(const auto &t, auto... v) {print_(t); if (sizeof...(v)) cerr << ", "; debug_(v...);}
#define debug(x...) cerr << __LINE__ << ": " <<  "[" << #x << "] = ["; debug_(x)

#define all(a) (a).begin(), (a).end()
#define rall(a) (a).rbegin(), (a).rend()

template <typename T> using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
template <typename K, typename V> using ordered_map = tree<K, V, less<K>, rb_tree_tag, tree_order_statistics_node_update>;
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
