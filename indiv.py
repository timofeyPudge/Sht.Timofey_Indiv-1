import heapq
from collections import defaultdict, Counter
import math  # Импортируем модуль math для использования log2


# Шаг 1: Подсчет частот
def calculate_frequencies(text):
    # Фильтруем текст, оставляя только буквы и пробелы
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ")
    filtered_text = ''.join(filter(lambda x: x in allowed_chars, text))
    frequencies = Counter(filtered_text)
    total_chars = len(filtered_text)
    return frequencies, total_chars


# Шаг 2: Построение дерева Хаффмана с алфавитом {0,1,2,3}
class HuffmanNode:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.children = []
        self.code = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies):
    heap = [HuffmanNode(symbol=symbol, freq=freq) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        children = [heapq.heappop(heap) for _ in range(min(4, len(heap)))]
        parent = HuffmanNode(freq=sum(child.freq for child in children))
        parent.children = children
        heapq.heappush(heap, parent)

    return heap[0]


def assign_codes(node, current_code=""):
    if node.symbol is not None:
        return {node.symbol: current_code}
    codes = {}
    for idx, child in enumerate(node.children):
        codes.update(assign_codes(child, current_code + str(idx)))
    return codes


# Шаг 3: Вычисление средней длины и избыточности
def calculate_avg_length_and_redundancy(codes, frequencies, total_chars):
    avg_length = sum(len(codes[symbol]) * freq for symbol, freq in frequencies.items()) / total_chars
    entropy = -sum((freq / total_chars) * math.log2(freq / total_chars) for freq in frequencies.values() if freq > 0)
    redundancy = avg_length - entropy
    return avg_length, redundancy


# Пример
text = """НО ТОТЧАС ЖЕ ОН ВСПОМНИЛ ДАННОЕ КНЯЗЮ АНДРЕЮ ЧЕСТНОЕ СЛОВО НЕ БЫВАТЬ У
КУРАГИНА НО ТОТЧАС ЖЕ КАК ЭТО БЫВАЕТ С ЛЮДЬМИ НАЗЫВАЕМЫМИ БЕСХАРАКТЕРНЫМИ ЕМУ
ТАК СТРАСТНО ЗАХОТЕЛОСЬ ЕЩЕ РАЗ ИСПЫТАТЬ ЭТУ СТОЛЬ ЗНАКОМУЮ ЕМУ БЕСПУТНУЮ ЖИЗНЬ
ЧТО ОН РЕШИЛСЯ ЕХАТЬ И ТОТЧАС ЖЕ ЕМУ ПРИШЛА В ГОЛОВУ МЫСЛЬ ЧТО ДАННОЕ СЛОВО
НИЧЕГО НЕ ЗНАЧИТ ПОТОМУ ЧТО ЕЩЕ ПРЕЖДЕ ЧЕМ КНЯЗЮ АНДРЕЮ ОН ДАЛ ТАКЖЕ КНЯЗЮ
АНАТОЛЮ СЛОВО БЫТЬ У НЕГО НАКОНЕЦ ОН ПОДУМАЛ ЧТО ВСЕ ЭТИ ЧЕСТНЫЕ СЛОВА ТАКИЕ
УСЛОВНЫЕ ВЕЩИ НЕ ИМЕЮЩИЕ НИКАКОГО ОПРЕДЕЛЕННОГО СМЫСЛА ОСОБЕННО ЕЖЕЛИ
СООБРАЗИТЬ ЧТО МОЖЕТ БЫТЬ ЗАВТРА"""

frequencies, total_chars = calculate_frequencies(text)
huffman_tree = build_huffman_tree(frequencies)
codes = assign_codes(huffman_tree)
avg_length, redundancy = calculate_avg_length_and_redundancy(codes, frequencies, total_chars)

print("Частоты символов:", frequencies)
print("Коды Хаффмана:", codes)
print("Средняя длина кодового слова:", avg_length)
print("Избыточность кода:", redundancy)
