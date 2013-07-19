opentxtr
========

open-source software for talking to the ultra-cheap txtr Beagle e-reader

from a 600x800 pixel pgm image, do

./imgpipe grayscale.pgm | ./zpipe > page.gz

and tweak the beagle_client.py script.


some random notes about the protocol
------------------------------------

display=V110 => size=600x800 (10 pixel progress bar at bottom)
1 page = (800*600)/2 + 64 (4bpp, lowest bit always clear)

clean input stream
PING

reset everything
VIRGIN
VIRGINOK

get device info
INFO
.....
INFOOK

get memory usage info
MEMORY
.....
MEMORYOK

get books
GETBOOKS
BOOK ID=....
.....
GETBOOKSOK

disconnect
QUIT

pair info
GETPARTNER
NOPARNTER

set pair info
PARTNER ID=8D982A15C9C49900
PARTNEROK

send book
BOOK ID=8000000002DF9300
BOOKOK

TITLE V2hpdGUgRmFuZw
TITLEOK

AUTHOR TG9uZG9uLCBKYWNr
AUTHOROK

PAGE 1
data.....
PAGEOK

ENDBOOK
ENDBOOKOK

deletebook
DELETEBOOK ID=....
DELETEBOOKOK

utilitypage?
UTILITYPAGE 1
.....
PAGEOK
