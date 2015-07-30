### ReadMe contents ###

on this page...
- [qualifier](#qualifier)
- [process overview](#codecontext-overview)
- [contacts](#contacts)
- [license](#license)


### Qualifier ###

This is old code recently updated a bit. It was one of my first python projects; there's still lots of evidence of my camelCase java background.


### Code/context overview ###

Patrons sometimes request, from our old [library catalog](https://josiah.brown.edu), items which are stored at the [Annex](http://library.brown.edu/about/annex/), the Brown Library's offsite storage facility.

This python code uses the [III millennium](http://www.iii.com/products/millennium) command-line interface. It acts as if a staff-person is sitting at a terminal and connects to the integrated-library-system server via ssh, and then executes a series of steps to:
- prepare a file of pageslips for recent requests for items that are at the Annex
- transfer that file to the server that runs the Annex inventory control software

The python tool used to perform this magic is the wonderful [pexpect](https://github.com/pexpect/pexpect) library.

A [separate script](https://github.com/birkin/annex_process_pageslips) periodically checks to see if a new file has arrived, and parses that pageslip file into the files needed for the Annex's inventory-control software.


### Contacts ###

Domain contact: bonnie_buzzell@brown.edu

Programmer: birkin_diana@brown.edu


### License ###

The MIT License (MIT)

Copyright (c) 2015 Brown University Library

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
