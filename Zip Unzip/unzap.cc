#include <iostream>

#include "huffman.h"

int main(int argc, char *argv[]) {
    if (argc < 3 || argc > 3) {
        std::cerr << "Usage: /autograder/source/tests/unzap "
        << "<zapfile> <outputfile>" << std::endl;
        return 1;
    }
    std::ifstream ifs(argv[1], std::ios::in |
                    std::ios::binary);
    if (!ifs) {
        std::cerr << "Error: cannot open zap file " << argv[1] << std::endl;
        return 1;
    }
    std::ofstream ofs(argv[2], std::ios::out |
                    std::ios::trunc);
    Huffman::Decompress(ifs, ofs);

    std::cout << "Decompressed zap file " << argv[1] <<
    " into output file " << argv[2] << std::endl;
}
