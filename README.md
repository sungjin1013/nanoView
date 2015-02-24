# pileup.js
Interactive in-browser track viewer

## Quickstart

    git clone https://github.com/danvk/pileup.js.git
    cd pileup.js
    npm install
    grunt prod

To play with the demo, you'll need [RangeHTTPServer][rs], which adds support
for byte range requests to SimpleHTTPServer:

    pip install rangehttpserver
    python -m RangeHTTPServer

Then open `http://localhost:8000/playground.html` in your browser of choice.

## Development

Run the tests from the command line:

    grunt test

Run the tests in a real browser:

    grunt browsertests
    open tests/runner.html

To iterate on code while running the type checker:

    grunt watchFlow

To continuously regenerate the combined JS, run:

    grunt watchFlowProd

[rs]: https://github.com/danvk/RangeHTTPServer