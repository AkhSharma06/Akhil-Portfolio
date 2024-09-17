#ifndef HUFFMAN_H_
#define HUFFMAN_H_

#include <array>
#include <cstddef>
#include <cctype>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <bitset>
#include <map>
#include <stack>

#include "bstream.h"
#include "pqueue.h"

class HuffmanNode {
 public:
  explicit HuffmanNode(char ch, size_t freq,
                       HuffmanNode *left = nullptr,
                       HuffmanNode *right = nullptr)
      : ch_(ch), freq_(freq), left_(left), right_(right) { }


  bool IsLeaf() {
    // Node is a leaf if it doesn't have any children
    return left_ == nullptr && right_ == nullptr;
  }

  bool operator < (const HuffmanNode &n) const {
    // In case of equality, make it deterministic based on character
    if (freq_ == n.freq_)
      return ch_ < n.ch_;
    // Otherwise compare frequencies
    return freq_ < n.freq_;
  }

  size_t freq() { return freq_; }
  size_t data() { return ch_; }
  HuffmanNode* left() { return left_; }
  HuffmanNode* right() { return right_; }
  void SetLeft(HuffmanNode* left){
    left_ = left;
  }
  void SetRight(HuffmanNode* right) {
    right_ = right;
  }

 private:
  char ch_;
  size_t freq_;
  HuffmanNode *left_, *right_;
  
};

class HuffmanCompMin {
 public:
  bool operator()(HuffmanNode *x, HuffmanNode *y) const {
    if (x->freq() == y->freq()) return x->data() < y->data();
    return x->freq() < y->freq();
  }
};

class Huffman {
 public:
  static void Compress(std::ifstream &ifs, std::ofstream &ofs);

  static void Decompress(std::ifstream &ifs, std::ofstream &ofs);

  

 private:
  std::vector<HuffmanNode*> vec;
  std::string output;
  std::string code_table; // 128 ASCII characters
  void CountFrequency(std::ifstream &ifs);
  void HuffmanOutput(HuffmanNode* root);
  char GetCharacter(HuffmanNode* node);
  void CodeTable(HuffmanNode* root);
  std::map<char, std::string> map;
  std::stack<HuffmanNode* > node_stack;
  std::stack<std::string> code_stack;
  int count = 0;
  int iterate = 0;
  std::string characters;

  // Helper methods...
  void BuildingTree();
  void Encode(std::ifstream &ifs, BinaryOutputStream &bos);
  PQueue<HuffmanNode*, HuffmanCompMin> node_pq;
  HuffmanNode* MakeNode(BinaryInputStream &bis);
  void Uncode(BinaryInputStream &bis, HuffmanNode* root, HuffmanNode* top);
  void print(HuffmanNode* root) {
  if (!root) {
    return;
  }
  if (root->data() == 0) {
    std::cout << "0" << std::endl;
  } else {
    std::cout << char(root->data()) << std::endl;
  }
  print(root->left());
  print(root->right());
}
};


void Huffman::CountFrequency(std::ifstream &ifs) {
  int frequencies[128] = {0};
  
  std::string lines;
    //ifs.open("all_ABC.txt");
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
}

void Huffman::HuffmanOutput(HuffmanNode* root) {
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

void Huffman::CodeTable(HuffmanNode* root) {
  HuffmanNode* node = root;
  std::string code;
  // Firstly going in loop until the stack is empty
  while (1) {
    // Going in a loop until a leaf is found and inserted into map
    while(1) {
      // Checking if node is a leaf and inserting it into a map with its assigned code
      if (node->IsLeaf()) {
        map.insert(std::pair<char, std::string>(static_cast<char>(node->data()), code));
        break;
      }
      // If the node has a right child, push it into the stack and push its code into the code_stack
      if (node->right()) {
        code_stack.push(code);
        node_stack.push(node->right());
      }
      // If the node has a left child, make the current node its left child and put a 0 into the code
      if (node->left()) {
        node = node->left();
        code.append("0");
      }
    }
    // Once a leaf is found and it is inserted, while the node_stack is not empty, set the new node to be the right child (which is the top of the stack)
    // And append the 1 (to represent a right child)
    // Then add the code stored in the stack to the local code and put a 1 to represent another right move
    if (!node_stack.empty()) {
      node = node_stack.top();
      if (!node->IsLeaf()) {
        code.append("1");
      }
      code = code_stack.top();
      code.append("1");
      code_stack.pop();
      node_stack.pop();
    } else {
      break;
    }
  }
}



//  THINGS I ADDED

void Huffman::BuildingTree() { 
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
}

void Huffman::Encode(std::ifstream &ifs, BinaryOutputStream &bos) {
  std::string encoded_output;  // for output string
  for (int i = 0; i < (signed)characters.size(); i++) {
    encoded_output.append(map[(int)characters[i]]);
  }

  // put the count into binary stream first
  bos.PutInt((signed)characters.size());
  // put the encoded output into stream after
    for (int i = 0; i < (signed)encoded_output.length(); i++) {
      bos.PutBit(encoded_output[i]-48);
    }
}

void Huffman::Compress(std::ifstream &ifs, std::ofstream &ofs) {
  Huffman obj;
  // Counting the frequency of characters: returns a vector w/ HuffmanNodes
  obj.CountFrequency(ifs);
  // build the tree; not sure if i initialized the root correctly?
  obj.BuildingTree();

  // Outputting the huffman tree: output on ofs with bstream stuff
  obj.HuffmanOutput(obj.node_pq.Top());

  BinaryOutputStream bos(ofs);
  for (int i = 0; i < (signed)obj.output.length(); i++) {
    bos.PutBit(obj.output[i]-48);
  }
  // Building the coding table: make a coding table of an array(?)
  //std::cout << obj.count << std::endl;
  obj.CodeTable(obj.node_pq.Top());
  // Ouputting the encoded string
  obj.Encode(ifs, bos);
}

HuffmanNode* Huffman::MakeNode(BinaryInputStream &bis) {
  bool bit = bis.GetBit();
  HuffmanNode* node;
  char c;
  if (bit) {
    c = bis.GetChar();
    node = new HuffmanNode(c,0);
  } else {
    node = new HuffmanNode(0,0);
  }

  if (!bit) {
    node->SetLeft(MakeNode(bis));
    node->SetRight(MakeNode(bis));
  }
  return node;
}

void Huffman::Uncode(BinaryInputStream &bis, HuffmanNode* root, HuffmanNode* top) {
  if(root->IsLeaf()) {
    output.push_back(root->data());
    iterate++;
    return;
  }
  bool bit = bis.GetBit();
  if(bit) Uncode(bis, root->right(), top);
  else Uncode(bis, root->left(), top);
  if(iterate == count) return;
  if(root == top) Uncode(bis, root, top);
  else return;
}

void Huffman::Decompress(std::ifstream &ifs, std::ofstream &ofs) {
  Huffman obj;
  BinaryInputStream bis(ifs);
  obj.node_pq.Push(obj.MakeNode(bis));

  obj.count = bis.GetInt();

  obj.Uncode(bis, obj.node_pq.Top(), obj.node_pq.Top());

  for (int i = 0; i < (signed)obj.output.length(); i++) {
    ofs.put(obj.output[i]);
  }
}



#endif  // HUFFMAN_H_

