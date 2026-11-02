import math
from collections import Counter


from task9 import build_huffman, encode

def analyze_text():
    # Пункт 10.1: Русский текст длиной более 300 символов
    sample_text = (
        "Кибербезопасность — это практика защиты критически важных систем, "
        "сетей, мобильных приложений и конфиденциальных данных от цифровых угроз. "
        "В условиях стремительного развития информационных технологий вопросы "
        "криптографической защиты и эффективного сжатия данных приобретают "
        "первостепенное значение для обеспечения информационной безопасности "
        "как крупных корпораций, так и рядовых пользователей в повседневной жизни."
    )
    
    n_total = len(sample_text)
    text_freq = Counter(sample_text)

    # Пункт 10.2: Расчет параметров
    h_x = -sum((cnt / n_total) * math.log2(cnt / n_total) for cnt in text_freq.values())
    
    t_tree, t_codes = build_huffman(text_freq)
    encoded_bits = encode(sample_text, t_codes)
    
    l_avg = sum((text_freq[char] / n_total) * len(code) for char, code in t_codes.items())
    
    efficiency = (h_x / l_avg) * 100
    redundancy = (1 - h_x / l_avg) * 100


    alphabet_size = len(text_freq)
    fixed_bit_len = math.ceil(math.log2(alphabet_size))
    volume_fixed_bits = n_total * fixed_bit_len
    volume_huffman_bits = len(encoded_bits)

    k_compression = volume_fixed_bits / volume_huffman_bits
    savings_percent = (1 - volume_huffman_bits / volume_fixed_bits) * 100


    overhead_bits = 45 * 8 
    total_with_overhead = volume_huffman_bits + overhead_bits
    k_real = volume_fixed_bits / total_with_overhead

 
    print("=== ЗАДАЧА 10: Исследование реального текста ===")
    print(f"Длина текста: {n_total} символов")
    print(f"Размер алфавита: {alphabet_size} уникальных симво символов")
    print("-" * 45)
    print(f"Энтропия H(X): {h_x:.4f} бит/символ")
    print(f"Средняя длина кодового слова L̄: {l_avg:.4f} бит/символ")
    print(f"Эффективность (η): {efficiency:.2f}%")
    print(f"Избыточность (R): {redundancy:.2f}%")
    print("-" * 45)
    print(f"Объем при фиксированном коде ({fixed_bit_len} бит/символ): {volume_fixed_bits} бит")
    print(f"Объем сжатых данных Хаффмана: {volume_huffman_bits} бит")
    print(f"Коэффициент сжатия (Kc) без заголовка: {k_compression:.4f}")
    print(f"Процент сокращения объема (S): {savings_percent:.2f}%")
    print("-" * 45)
    print(f"Служебные данные (дерево): ~{overhead_bits} бит (45 байт)")
    print(f"Реальный объем с заголовком: {total_with_overhead} бит")
    print(f"Реальный коэффициент сжатия (Kc): {k_real:.4f}")

if name == "main":
    analyze_text()