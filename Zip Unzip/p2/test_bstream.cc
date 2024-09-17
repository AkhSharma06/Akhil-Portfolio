#include <gtest/gtest.h>

#include <cstdio>
#include <fstream>
#include <string>
#include <iostream>
#include <bitset>
#include "bstream.h"

TEST(BStream, input) {
  std::string filename{"test_bstream_input"};
  std::string words;

  const unsigned char val[] = {
    0x58, 0x90, 0xab, 0x08,
    0x00, 0x4e, 0xdb, 0x40,
  };
  // Equivalent in binary is:
  // 0101100010010000101010110000100000000000010011101101101101000000
  // ^5  ^8  ^9  ^0  ^a  ^b  ^0  ^8  ^0  ^0  ^4  ^e  ^d  ^b  ^4  ^0

  // Write this to a file
  std::ofstream ofs(filename, std::ios::out |
                    std::ios::trunc |
                    std::ios::binary);
  ofs.write(reinterpret_cast<const char *>(val), sizeof(val));
  ofs.close();

  // Read it back in binary format
  std::ifstream ifs(filename, std::ios::in |
                    std::ios::binary);
  BinaryInputStream bis(ifs);

  // Make sure that we reading the binary in the correct order
  EXPECT_EQ(bis.GetBit(), 0);
  EXPECT_EQ(bis.GetBit(), 1);
  EXPECT_EQ(bis.GetChar(), 0x62);  // 01100010
  EXPECT_EQ(bis.GetChar(), 0x42);  // 01000010
  EXPECT_EQ(bis.GetBit(), 1);
  EXPECT_EQ(bis.GetInt(), 0x58400276);  // 01011000010000000000001001110110
  
  
  ifs.close();
  //std::remove(filename.c_str());
}

TEST(BStream, output) {
  std::string filename{"test_bstream_output"};
  std::string words;
  std::ofstream ofs(filename, std::ios::out |
                    std::ios::trunc |
                    std::ios::binary);
  BinaryOutputStream bos(ofs);
  bos.PutChar('a');
  bos.PutChar('b');
  bos.PutChar('#');
  bos.PutInt(1);
  bos.PutInt(5);
  ofs.close();

  unsigned char val[12];
  std::ifstream ifs(filename, std::ios::in |
                    std::ios::binary);
  ifs.read(reinterpret_cast<char *>(val), sizeof(val));
  ifs.close();
  EXPECT_EQ(val[0], 'a');
  EXPECT_EQ(val[1], 'b');
  EXPECT_EQ(val[2], '#');
  EXPECT_EQ(val[6], 1);
  EXPECT_EQ(val[10], 5);
  std::remove(filename.c_str());
}

int main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
