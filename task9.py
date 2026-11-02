import heapq
import math
from collections import Counter
from itertools import count


def build_huffman(freq):
    if not freq:
        raise ValueError("Пустой алфавит")
    

    if len(freq) == 1:
        char = list(freq.keys())[0]
        return char, {char: "0"}

    order = count()
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    heapq.heapify(heap)
    
    if not heap:
        raise ValueError("Все частоты нулевые")
        
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))
        
    tree = heap[0][2]
    codes = {}
    
    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")
            
    walk(tree)
    return tree, codes

def encode(text, codes):
    return "".join(codes[s] for s in text)

def decode(bits, tree):
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)
        
    result, node = [], tree
    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree
            
    if node is not tree:
        raise ValueError("Неполное кодовое слово")
    return "".join(result)


if name == "main":
    print("=== ЗАДАЧА 9: Тест на сообщении 'ABCADE' ===")
    text = "ABCADE"
    freq = Counter(text)
    
    total_len = len(text)
    entropy = -sum((cnt / total_len) * math.log2(cnt / total_len) for cnt in freq.values())
    
    tree, codes = build_huffman(freq)
    bits = encode(text, codes)
    
    print("Частоты символов:", dict(freq))
    print("Кодовые слова:", codes)
    print("Закодированная битовая строка:", bits)
    print("Длина строки:", len(bits), "бит")
    print(f"Энтропия H(X): {entropy:.4f} бит/символ")
    
    decoded_text = decode(bits, tree)
    print("Декодированный текст:", decoded_text)
    
    assert decoded_text == text, "Ошибка декодирования!"
    print("Проверка прошла успешно: decode(encode(text)) == text")