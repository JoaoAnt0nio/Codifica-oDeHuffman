import heapq
import os
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  
        self.freq = freq
        self.left = None
        self.right = None

    # Comparação para a fila de prioridade (heapq)
    # Menor frequência tem maior prioridade
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(text_segment):
    
    # Separa por espaços para identificar as palavras
    words = text_segment.split()
    return Counter(words)

def build_huffman_tree(freq_dict):
    
    heap = []
    
    # Cria nós folha para cada palavra e adiciona ao heap
    for word, freq in freq_dict.items():
        node = HuffmanNode(word, freq)
        heapq.heappush(heap, node)

    # Combina os nós até restar apenas a raiz
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(node, prefix="", code_map={}):
    
    if node is None:
        return

    # Se for folha, salva o código
    if node.char is not None:
        code_map[node.char] = prefix
    
    generate_codes(node.left, prefix + "0", code_map)
    generate_codes(node.right, prefix + "1", code_map)
    
    return code_map

def serialize_tree_structure(node, level=0):
    
    if node is None:
        return ""
    
    result = ""
    indent = "  " * level
    
    if node.char is not None:
        result += f"{indent}- Folha: '{node.char}' ({node.freq})\n"
    else:
        result += f"{indent}- Nó Interno ({node.freq})\n"
    
    result += serialize_tree_structure(node.left, level + 1)
    result += serialize_tree_structure(node.right, level + 1)
    
    return result

def setup_environment():
    
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Diretório 'data/' criado.")

    input_path = os.path.join('data', 'input.dat')
    
def main():
    setup_environment()
    
    input_file = os.path.join('data', 'input.dat')
    output_file = os.path.join('data', 'output.dat')
    
    print(f"Lendo de: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Erro: input.dat não encontrado.")
        return

    # Separa os textos por linha em branco
    text_segments = content.split('\n\n')
    
    output_content = []

    for i, text in enumerate(text_segments):
        if not text.strip(): continue # Pula segmentos vazios
        
        # 1. Calcular frequências e montar árvore
        freqs = build_frequency_dict(text)
        root = build_huffman_tree(freqs)
        
        # 2. Gerar códigos
        codes = generate_codes(root, "", {})
        
        # 3. Comprimir o texto
        words = text.split()
        compressed_text = "".join([codes[word] for word in words])
        
        # 4. Preparar saída formatada
        segment_output = f"=== TEXTO {i+1} ===\n"
        segment_output += f"Original: {text.strip()}\n\n"
        
        segment_output += "--- Estrutura da Árvore ---\n"
        segment_output += serialize_tree_structure(root)
        
        segment_output += "\n--- Tabela de Códigos ---\n"
        for word, code in codes.items():
            segment_output += f"'{word}': {code}\n"
            
        segment_output += f"\n--- Texto Comprimido (Binário) ---\n"
        segment_output += f"{compressed_text}\n"
        segment_output += "="*40 + "\n"
        
        output_content.append(segment_output)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_content))
        
    print(f"Processamento concluído! Resultados salvos em: {output_file}")

if __name__ == "__main__":
    main()