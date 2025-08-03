#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

vector<int> find_minimal_max_sequence(int n, int p, int q) {
    vector<int> best_sequence;
    int min_max_element = INT_MAX;

    for (int d = 1; d <= 50; ++d) {
        for (int start = min(p, q) - (n - 1) * d; start <= max(p, q); ++start) {
            vector<int> sequence;
            for (int i = 0; i < n; ++i) {
                sequence.push_back(start + i * d);
            }

            if (find(sequence.begin(), sequence.end(), p) != sequence.end() &&
                find(sequence.begin(), sequence.end(), q) != sequence.end()) {
                
                int max_element = sequence.back();

                if (max_element < min_max_element) {
                    min_max_element = max_element;
                    best_sequence = sequence;
                }
            }
        }
    }

    return best_sequence;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n, p, q;
        cin >> n >> p >> q;

        vector<int> result = find_minimal_max_sequence(n, p, q);

        if (result.empty()) {
            cout << "No valid sequence found" << endl;
        } else {
            for (int num : result) {
                cout << num << " ";
            }
            cout << endl;
        }
    }

    return 0;
}