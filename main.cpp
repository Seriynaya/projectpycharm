// M_card(x) = x[0..3] ++ " " ++ x[4..5] ++ "** **** " ++ x[12..15]
// M_acc(x)  = "**" ++ x[n-4..n-1]
// F(T,s) = { t ∈ T | t.state = s }, O(n)
// F_c(T,c) = { t ∈ T | t.currency_code = c }, O(n)
// S(T) = stable_sort(T, key=date), O(n log n)
// Search(T,q) = { t ∈ T | q ⊆ t.description }, O(n·|q|)
// TopK(T,k): nth_element O(n) + sort O(k log k) → O(n + k log k)
// G(a,b) = { fmt16(i) | i ∈ [a,b] }, fmt16(i) = zero_pad(i,16), group(4)
// H(T) → unordered_map<key, vector<T>>, O(n) build, O(1) lookup

#include <iostream>
#include <vector>
#include <string>
#include <string_view>
#include <algorithm>
#include <unordered_map>
#include <sstream>
#include <iomanip>
#include <functional>
#include <cstdint>
#include <optional>
#include <span>
#include <ranges>
#include <numeric>
#include <utility>
#include <iterator>

struct Transaction {
    int id{};
    std::string state;           // EXECUTED | CANCELED | PENDING
    std::string date;            // YYYY-MM-DDTHH:MM:SS
    std::string description;
    double amount{};
    std::string currency_code;
    std::string from_account;
    std::string to_account;
};

// is_digit(c) = c ∈ ['0','9']
constexpr bool is_digit(char c) noexcept { return c >= '0' && c <= '9'; }

// clamp_k(k, n) = min(max(k, 0), n)
constexpr int clamp_k(int k, int n) noexcept { return k < 0 ? 0 : (k > n ? n : k); }

// |T| = 14
static std::vector<Transaction> DATA = {
    {1, "EXECUTED", "2024-01-15T12:30:00", "Transfer to organization", 31957.58, "RUB",
     "Visa Platinum 7000792289606361", "Account 73654108430135874305"},
    {2, "EXECUTED", "2024-02-20T08:00:00", "Account to account transfer", 500.00, "USD",
     "Account 19708645243227258542", "Account 75651667383060284188"},
    {3, "CANCELED", "2024-03-01T14:22:10", "Currency purchase", 1200.00, "EUR",
     "Maestro 1596837868705199", "Account 64686473678894779589"},
    {4, "EXECUTED", "2024-03-10T09:15:30", "Card to card transfer", 75000.00, "RUB",
     "Visa Classic 6831982476737658", "Visa Gold 5999414228426353"},
    {5, "PENDING", "2024-03-15T16:45:00", "Service payment", 3200.50, "RUB",
     "MasterCard 7158300734726758", "Account 35383033474447895560"},
    {6, "EXECUTED", "2024-04-01T10:00:00", "Transfer to organization", 250.00, "USD",
     "Visa Platinum 8990922113665229", "Account 55667788990011223344"},
    {7, "CANCELED", "2024-04-12T11:30:00", "Refund", 15000.00, "RUB",
     "Account 41421553129062836915", "Visa Classic 4195191172583802"},
    {8, "EXECUTED", "2024-05-05T07:20:00", "Account to account transfer", 100.00, "EUR",
     "Account 98765432101234567890", "Account 12345678901234567890"},
    {9, "EXECUTED", "2024-05-18T19:00:00", "Product purchase", 850.00, "USD",
     "Visa Gold 5999414228426353", "Account 90887766554433221100"},
    {10, "PENDING", "2024-06-01T13:10:00", "Subscription payment", 9.99, "USD",
      "MasterCard 3152479541115065", "Account 64686473678894779589"},
    {11, "EXECUTED", "2024-06-15T08:45:00", "Transfer to organization", 42000.00, "RUB",
      "Account 73654108430135874305", "Account 11223344556677889900"},
    {12, "CANCELED", "2024-07-03T22:00:00", "Operation canceled", 5500.00, "RUB",
      "Visa Platinum 7000792289606361", "Account 19708645243227258542"},
    {13, "EXECUTED", "2024-07-20T15:30:00", "Card to card transfer", 300.00, "EUR",
      "Maestro 1596837868705199", "Visa Classic 6831982476737658"},
    {14, "EXECUTED", "2024-08-01T00:00:01", "Salary deposit", 120000.00, "RUB",
      "Account 55667788990011223344", "Visa Platinum 8990922113665229"},
};

// M_card(x) = x[0..3] ++ " " ++ x[4..5] ++ "** **** " ++ x[12..15], |x|=16
[[nodiscard]] std::string mask_card(std::string_view raw) {
    std::string d;
    d.reserve(20);
    for (const char c : raw) if (is_digit(c)) d += c;
    if (d.size() != 16) return std::string(raw);
    // M(d) = d[0..3] " " d[4..5] "** **** " d[12..15]
    return d.substr(0, 4) + " " + d.substr(4, 2) + "** **** " + d.substr(12, 4);
}

// M_acc(x) = "**" ++ x[n-4..n-1], |x| >= 4
[[nodiscard]] std::string mask_account(std::string_view raw) {
    std::string d;
    d.reserve(24);
    for (const char c : raw) if (is_digit(c)) d += c;
    if (d.size() < 4) return std::string(raw);
    return "**" + d.substr(d.size() - 4);
}

// P(x) = starts_with(x, "Account") ? mask_account(x) : mask_card(x)
[[nodiscard]] std::string mask_identifier(std::string_view s) {
    if (s.starts_with("Account")) {
        auto pos = s.find_last_of(' ');
        if (pos == std::string_view::npos) return mask_account(s);
        auto prefix_label = s.substr(0, pos);
        auto digits_part = s.substr(pos + 1);
        std::string d;
        for (const char c : digits_part) if (is_digit(c)) d += c;
        if (d.size() < 4) return std::string(s);
        return std::string(prefix_label) + " **" + d.substr(d.size() - 4);
    }
    auto pos = s.find_last_of(' ');
    if (pos == std::string_view::npos) return mask_card(s);
    auto prefix_label = s.substr(0, pos);
    auto digits_part = s.substr(pos + 1);
    std::string masked = mask_card(digits_part);
    return std::string(prefix_label) + " " + masked;
}

// F(T,s) = { t ∈ T | t.state = s }, O(n)
[[nodiscard]] std::vector<Transaction>
filter_by_state(std::span<const Transaction> T, std::string_view state) {
    std::vector<Transaction> R;
    R.reserve(T.size());
    for (const auto& t : T)
        if (t.state == state) R.push_back(t);
    return R;
}

// F_c(T, code) = { t ∈ T | t.currency_code = code }, O(n)
[[nodiscard]] std::vector<Transaction>
filter_by_currency(std::span<const Transaction> T, std::string_view code) {
    std::vector<Transaction> R;
    R.reserve(T.size());
    for (const auto& t : T)
        if (t.currency_code == code) R.push_back(t);
    return R;
}

// S(T, desc) = sort(T, λ(a,b) = desc ? a.date > b.date : a.date < b.date), O(n log n)
void sort_by_date(std::vector<Transaction>& T, bool descending = true) {
    if (descending) {
        std::ranges::sort(T, std::ranges::greater{}, &Transaction::date);
    } else {
        std::ranges::sort(T, std::ranges::less{}, &Transaction::date);
    }
}

// Search(T, q) = { t ∈ T | q ⊆ t.description }, O(n·|q|)
[[nodiscard]] std::vector<Transaction>
search_descriptions(std::span<const Transaction> T, std::string_view query) {
    std::vector<Transaction> R;
    for (const auto& t : T)
        if (t.description.find(query) != std::string::npos)
            R.push_back(t);
    return R;
}

// G(a,b): ∀ i ∈ [a,b], yield fmt16(i)
// fmt16(i) = zero_pad(i, 16), split every 4: "XXXX XXXX XXXX XXXX"
class CardNumberGenerator {
    int64_t cur_;
    int64_t end_;

public:
    struct Sentinel {};

    class Iterator {
        int64_t cur_;
    public:
        using iterator_category = std::input_iterator_tag;
        using value_type        = std::string;
        using difference_type   = std::ptrdiff_t;
        using pointer           = const std::string*;
        using reference         = std::string;

        explicit Iterator(int64_t val) noexcept : cur_(val) {}

        // fmt(i) = sprintf("%016lld", i), insert ' ' at {4,9,14}
        [[nodiscard]] std::string operator*() const {
            std::ostringstream oss;
            oss << std::setw(16) << std::setfill('0') << cur_;
            std::string s = oss.str();
            return s.substr(0, 4) + " " + s.substr(4, 4) + " " + s.substr(8, 4) + " " + s.substr(12, 4);
        }

        Iterator& operator++() noexcept { ++cur_; return *this; }
        Iterator operator++(int) noexcept { auto tmp = *this; ++cur_; return tmp; }

        // i ≤ end ↔ not done
        [[nodiscard]] bool operator==(Sentinel) const noexcept { return false; }
        [[nodiscard]] bool operator!=(Sentinel) const noexcept { return true; }
        [[nodiscard]] int64_t value() const noexcept { return cur_; }
    };

    // i ∈ [start, end]
    CardNumberGenerator(int64_t start, int64_t end) noexcept : cur_(start), end_(end) {}

    [[nodiscard]] Iterator begin() const noexcept { return Iterator(cur_); }
    [[nodiscard]] int64_t  end_value() const noexcept { return end_; }

    // range-based for: begin/end with sentinel check via has_next pattern
    // ∀ i ∈ [cur_, end_]
    void for_each(const std::function<void(const std::string&)>& fn) const {
        for (int64_t i = cur_; i <= end_; ++i) {
            Iterator it(i);
            fn(*it);
        }
    }

    [[nodiscard]] bool has_next() const noexcept { return cur_ <= end_; }

    [[nodiscard]] std::string next() {
        Iterator it(cur_++);
        return *it;
    }
};

static void print_transaction(const Transaction& t) {
    std::cout << "  [" << t.id << "] " << t.date.substr(0, 10) << " | "
              << t.state << " | " << t.description << "\n"
              << "       " << std::fixed << std::setprecision(2)
              << t.amount << " " << t.currency_code << "\n"
              << "       " << mask_identifier(t.from_account)
              << " -> " << mask_identifier(t.to_account) << "\n";
}

static void print_transactions(std::span<const Transaction> T) {
    if (T.empty()) {
        std::cout << "  (empty)\n";
        return;
    }
    for (const auto& t : T) print_transaction(t);
    // Σ = Σ_{t ∈ T} t.amount
    const double total = std::accumulate(T.begin(), T.end(), 0.0,
        [](double acc, const Transaction& t) { return acc + t.amount; });
    std::cout << "  -----------------------------------\n"
              << "  |T| = " << T.size()
              << ", Σ = " << std::fixed << std::setprecision(2) << total << "\n";
}

// H_c(T) → unordered_map<currency_code, vector<T>>, O(n) build, O(1) lookup
[[nodiscard]] std::unordered_map<std::string, std::vector<Transaction>>
build_currency_index(std::span<const Transaction> T) {
    std::unordered_map<std::string, std::vector<Transaction>> idx;
    for (const auto& t : T) idx[t.currency_code].push_back(t);
    return idx;
}

// H_s(T) → unordered_map<state, vector<T>>, O(n) build, O(1) lookup
[[nodiscard]] std::unordered_map<std::string, std::vector<Transaction>>
build_state_index(std::span<const Transaction> T) {
    std::unordered_map<std::string, std::vector<Transaction>> idx;
    for (const auto& t : T) idx[t.state].push_back(t);
    return idx;
}

// TopK(T, k): nth_element O(n) + sort O(k log k) → O(n + k log k)
[[nodiscard]] std::vector<Transaction>
top_k_by_amount(std::span<const Transaction> T, int k) {
    if (k <= 0 || T.empty()) return {};
    std::vector<Transaction> copy(T.begin(), T.end());
    k = clamp_k(k, static_cast<int>(copy.size()));
    std::nth_element(copy.begin(), copy.begin() + k - 1, copy.end(),
        [](const Transaction& a, const Transaction& b) { return a.amount > b.amount; });
    copy.resize(static_cast<std::size_t>(k));
    std::ranges::sort(copy, std::ranges::greater{}, &Transaction::amount);
    return copy;
}

int main() {
#ifdef _WIN32
    std::system("chcp 65001 > nul 2>&1");
#endif

    // H_c, H_s: O(n) build
    auto cidx = build_currency_index(DATA);
    auto sidx = build_state_index(DATA);

    int choice = 0;
    while (true) {
        std::cout << "\n======================================\n"
                  << "  Bank Transactions\n"
                  << "======================================\n"
                  << "  1. Filter by state\n"
                  << "  2. Sort by date\n"
                  << "  3. Filter by currency\n"
                  << "  4. Search by description\n"
                  << "  5. Show masked cards\n"
                  << "  6. Generate card numbers\n"
                  << "  7. Top-K by amount\n"
                  << "  0. Exit\n"
                  << "--------------------------------------\n"
                  << "  Choice: ";

        if (!(std::cin >> choice)) break;
        std::cin.ignore(10000, '\n');

        if (choice == 0) break;

        if (choice == 1) {
            // F(T, state), O(1) via H_s
            std::cout << "  State (EXECUTED/CANCELED/PENDING): ";
            std::string st;
            std::getline(std::cin, st);
            if (auto it = sidx.find(st); it != sidx.end())
                print_transactions(it->second);
            else
                std::cout << "  (no transactions with this state)\n";
        }
        else if (choice == 2) {
            // S(T, desc?), O(n log n)
            std::cout << "  Descending? (1=yes, 0=no): ";
            int desc; std::cin >> desc;
            auto sorted = DATA;
            sort_by_date(sorted, desc == 1);
            print_transactions(sorted);
        }
        else if (choice == 3) {
            // F_c(T, code), O(1) via H_c
            std::cout << "  Currency (USD/EUR/RUB): ";
            std::string code;
            std::getline(std::cin, code);
            if (auto it = cidx.find(code); it != cidx.end())
                print_transactions(it->second);
            else
                std::cout << "  (no transactions in this currency)\n";
        }
        else if (choice == 4) {
            // Search(T, q), O(n·|q|)
            std::cout << "  Search query: ";
            std::string q;
            std::getline(std::cin, q);
            auto res = search_descriptions(DATA, q);
            print_transactions(res);
        }
        else if (choice == 5) {
            // ∀ t ∈ T: print M(t.from), M(t.to)
            for (const auto& t : DATA) {
                std::cout << "  [" << t.id << "] "
                          << mask_identifier(t.from_account) << " -> "
                          << mask_identifier(t.to_account) << "\n";
            }
        }
        else if (choice == 6) {
            // G(a, b), |b - a| ≤ 50
            std::cout << "  Range start: ";
            int64_t a; std::cin >> a;
            std::cout << "  Range end: ";
            int64_t b; std::cin >> b;
            if (b - a > 50) {
                std::cout << "  (max 50)\n";
                b = a + 49;
            }
            CardNumberGenerator gen(a, b);
            gen.for_each([](const std::string& card) {
                std::cout << "  " << card << "\n";
            });
        }
        else if (choice == 7) {
            // TopK(T, k): O(n + k log k)
            std::cout << "  K = ";
            int k; std::cin >> k;
            auto topk = top_k_by_amount(DATA, k);
            print_transactions(topk);
        }
    }

    std::cout << "  Done.\n";
    return 0;
}
