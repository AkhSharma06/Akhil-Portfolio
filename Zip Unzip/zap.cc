#include <iostream>

#include "huffman.h"

int main(int argc, char *argv[]) {
    if (argc < 3 || argc > 3) {
        std::cerr << "Usage: /autograder/source/tests/zap "
        << "<inputfile> <zapfile>" << std::endl;
        return 1;
    }
    std::ifstream ifs(argv[1]);
    if (!ifs) {
        std::cerr << "Error: cannot open input file " << argv[1] << std::endl;
        return 1;
    }
    std::ofstream ofs(argv[2], std::ios::out |
                    std::ios::trunc |
                    std::ios::binary);
    Huffman::Compress(ifs, ofs);

    std::cout << "Compressed input file " << argv[1] <<
    " into zap file " << argv[2] << std::endl;
}