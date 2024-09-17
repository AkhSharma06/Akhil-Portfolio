all: zap unzap test_bstream test_pqueue

zap: zap.cc huffman.h bstream.h pqueue.h
	g++ -Wall -Werror -std=c++11 -g \
	-o zap zap.cc

unzap: unzap.cc huffman.h bstream.h pqueue.h
	g++ -Wall -Werror -std=c++11 -g \
	-o unzap unzap.cc

test_bstream: test_bstream.cc bstream.h
	g++ -Wall -Werror -std=c++11 -g \
	-o test_bstream test_bstream.cc -pthread -lgtest

test_pqueue: test_pqueue.cc bstream.h
	g++ -Wall -Werror -std=c++11 -g \
	-o test_pqueue test_pqueue.cc -pthread -lgtest

clean:
	-rm -f zap *.zap
	-rm -f unzap *.unzap
	-rm -f test_bstream
	-rm -f test_pqueue