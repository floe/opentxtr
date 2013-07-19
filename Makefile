all: imgpipe zpipe

imgpipe: imgpipe.cc
	g++ -Wall -o $@ $^

zpipe: zpipe.c
	g++ -Wall -o $@ $^ -lz
