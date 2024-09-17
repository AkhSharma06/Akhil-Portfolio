#include <bitset>
#include <string>
#include <iostream>
 
int main()
{
  /*
  std::string bit_string;
  bit_string.append("0");
  bit_string.append("101100010");
  std::bitset<8> b1(bit_string);             // [0, 0, 1, 1, 0, 0, 1, 0]
  // string from position 2 till end
  std::bitset<8> b2(bit_string, 2);      // [0, 0, 0, 0, 0, 0, 1, 0]
 
  // string from position 2 till next 3 positions
  std::bitset<8> b3(bit_string, 2, 3);   // [0, 0, 0, 0, 0, 0, 0, 1]
   
  std::cout << bit_string << '\n';*/

  std::string code_table[100];
  std::string code;
  code.append("1");
  code.append("0");
  code.append("0");
  code.append("1");
  // setcode()

  code_table['A'] = code;

  std::cout << code_table['A'] << std::endl;
 
  return 0;
}