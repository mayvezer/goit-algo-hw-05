import timeit

def boyer_moore_search(text, pattern):
    def build_shift_table(pattern):
        table = {}
        for i in range(len(pattern) - 1):
            table[pattern[i]] = len(pattern) - 1 - i
        return table

    shift_table = build_shift_table(pattern)
    m = len(pattern)
    n = len(text)
    i = m - 1

    while i < n:
        j = m - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            k -= 1
            j -= 1
        if j == -1:
            return k + 1
        shift = shift_table.get(text[i], m)
        i += shift
    return -1

def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp_search(text, pattern, prime=101):
    n, m = len(text), len(pattern)
    d = 256
    h = pow(d, m - 1) % prime
    p = 0
    t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % prime
            if t < 0:
                t = t + prime
    return -1

def measure_time(algo, text, pattern):
    return timeit.timeit(lambda: algo(text, pattern), number=10)

if __name__ == "__main__":

    text1 = "Приклад тексту з першої статті про алгоритми"
    text2 = "Аналіз даних та пошук підрядків у великих масивах"
    
    patterns = {
        "existing": "алгоритми",
        "fake": "вигаданий_запит"
    }
    
    algos = [boyer_moore_search, kmp_search, rabin_karp_search]
    
    for text_name, text in [("Стаття 1", text1), ("Стаття 2", text2)]:
        print(f"\n--- {text_name} ---")
        for p_type, p_value in patterns.items():
            print(f"Тип підрядка: {p_type}")
            for algo in algos:
                time = measure_time(algo, text, p_value)
                print(f"{algo.__name__}: {time:.6f} сек")