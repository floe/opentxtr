#include <stdexcept>
#include <fstream>
#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>


uint8_t* zalloc( int bufsize ) {
	void* res = malloc(bufsize);
	memset(res,0,bufsize);
	return (uint8_t*)res;
}


uint8_t* data;
int width,height,size,bpp;

void init( int w, int h, int b ) {
	size = w*h*b;
	data = (uint8_t*)malloc(size);
	bpp    = b;
	width  = w;
	height = h;
}

void load( const char* path, const char* type, int maxbpp ) {

	int fwidth,fheight,fvalues;
	std::string magic,tmp;

	// open file with whitespace skipping
	std::ifstream myfile( path, std::ios::in );
	myfile >> std::skipws;

	// parse the header
	myfile >> magic;   myfile.ignore(1); if (myfile.peek() == '#') getline( myfile, tmp );
	myfile >> fwidth;  myfile.ignore(1); if (myfile.peek() == '#') getline( myfile, tmp );
	myfile >> fheight; myfile.ignore(1); if (myfile.peek() == '#') getline( myfile, tmp );
	myfile >> fvalues;

	if ((magic != type) || (fvalues >= (1<<(8*maxbpp))) || (fvalues < 1)) 
		throw std::runtime_error( std::string("load( ") + std::string(path) + std::string(" ): no valid PGM file") );

	// init the base class
	init( fwidth, fheight, maxbpp );

	// skip one byte, read the rest
	myfile.ignore( 1 );
	myfile.read( (char*)data, size );
	myfile.close( );
}


int main( int argc, char* argv[] ) {

	if (argc != 2)
		throw std::runtime_error("usage: imgpipe page.pgm");

	load(argv[1],"P5",1);

	if ((width != 600) || (height != 800)) 
		throw std::runtime_error("not a valid txtr Beagle page (PGM, 600x800)");

	uint8_t* output  = zalloc(size/2);
	uint8_t* padding = zalloc(64);

	for (int i = 0; i < size; i+=2) {
		uint8_t current = data[i] & 0xE0;
		current = current | ((data[i+1] & 0xE0) >> 4);
		output[i/2] = current;
	}

	std::cout.write( (char*)  output, size/2 );
	std::cout.write( (char*) padding,     64 );

	return 0;
}

