#include <vector>
#include <iostream>
#include <string>

#include "huffman.h"
std::string output;

void HuffmanOutput(HuffmanNode* root) {
  if (!root) {
    return;
  }
  std::string data;
  if (root->data() == 0) {
    output.append("0");
  } else {
    output.append("1");
    // need to go from decimal to binary because root->data() returns in type size_t so it will return 6
    data = std::bitset<8>(root->data()).to_string();
    output.append(data);
  }
  HuffmanOutput(root->left());
  HuffmanOutput(root->right());
  
}


int main(int argc, char *argv[]) {
    std::vector<HuffmanNode*> vec;
    /*vec.push_back(new HuffmanNode('C', 10));
    vec.push_back(new HuffmanNode('D', 15));
    vec.push_back(new HuffmanNode('E', 1));
    vec.push_back(new HuffmanNode('B', 20));
    vec.push_back(new HuffmanNode('A', 30));*/
    int frequencies[128] = {0};
    // frequencies[int('A')] = 3;
    // frequencies[int('B')] = 4;
    std::string characters;
    std::string lines;
    std::ifstream ifs;
    ifs.open("all_ABC.txt");
  if (!ifs.is_open()) {
    std::cerr << "Could not open file" << std::endl;
  }
  while (!ifs.eof()) {
    try
    {
      getline(ifs, lines);
    }
    catch(...)
    {
      break;
    }
    characters.append(lines);
  }
  
  for (size_t i = 0; i < characters.length(); i++) {
    frequencies[int(characters[i])] += 1;
  }
  for (int i = 0; i < 128; i++) {
    if (frequencies[i] != 0) {
      vec.push_back(new HuffmanNode(char(i), frequencies[i]));
    }
  }

    PQueue<HuffmanNode*, HuffmanCompMin> node_pq;
    for (int i = 0; i < (signed)vec.size(); i++) {
        node_pq.Push(vec[i]);
    }
    std::vector<HuffmanNode*> popped_vec;
    while (node_pq.Size() > 1) {
        for (int i = 0; i < 2; i++) {
            popped_vec.push_back(node_pq.Top());
            node_pq.Pop();
        }
        int freq = popped_vec[0]->freq() + popped_vec[1]->freq();
        node_pq.Push(new HuffmanNode(0, freq, popped_vec[0], popped_vec[1]));
        popped_vec.pop_back();
        popped_vec.pop_back();
    }
    
    
  for(size_t i = 0; i < vec.size(); i++) {
    std::cout << vec[i]->freq() << std::endl;
  }

    //std::cout << "A: " << frequencies['A'] << " B: " << frequencies['B'] << std::endl;
    Huffman huf;
    HuffmanOutput(node_pq.Top());
    std::cout << output << std::endl;
    
  
    /*std::cout << map['A'] << std::endl;
    std::cout << map['B'] << std::endl;
    std::cout << map['C'] << std::endl;
    std::cout << map['D'] << std::endl;
    std::cout << map['E'] << std::endl;*/

}