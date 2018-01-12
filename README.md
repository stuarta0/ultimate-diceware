## Ultimate Diceware

Using diceware to create passphrases is a novel, hands-on approach to improving your passwords. However one of the slower parts of the process is finding each word in the wordlist. While the official wordlist PDF is perfectly functional, it could still be more efficient and presentable. I decided to design a new layout to improve both lookup speed and aesthetic.

![Ultimate Diceware Page Layout](https://raw.githubusercontent.com/stuarta0/ultimate-diceware/master/docs/diceware-infographic.png)

The document is designed as follows:
- The first and second dice define the page number with positional, colour coded tabs based on the first number. This creates 6 pages for each coloured tab (e.g. 11, 12, 13, 14, 15 and 16). Position and colour make it easy to find the correct page without reading the page numbers.
- The third dice defines the row. Due to the whitespace surrounding the row number, it’s easy to glance at after locating the page.
- The fourth dice defines the column. After finding the row, the eyes can travel across the row to find the correct column.
- The fifth dice defines the Nth word in the grid cell. Once the cell is located, the line number of the words are easily recognisable by sight.

The page margins, text size and overall layout are designed to optimise information density and readability. The document is designed for A5 printing too, so whilst there’s still 36 pages like the original, it takes up half the space.

Each grid cell allows for two wordlists. For English speakers, the original diceware list is the primary and the EFF wordlist is the secondary. In other languages, the primary wordlist is presented in their language and the secondary list is the original diceware list for reference. In some cases there are two wordlists provided for a language such as Chinese (Pinyin and Wubi). In this case, the primary would be Pinyin and the secondary would be Wubi.

### Download

Completed PDF's are available in the dist directory of the repository.

### Compile

To create your own modified version, first copy the base template.svg (in sources) into your specific language folder. Make changes as required, ensuring you keep the XML object ID's. Finally, run ```python generate.py``` to generate the page SVG's.

Now that the page SVG's are created, you'll need to convert to PDF and merge to a single document. If you're on linux with Inkscape installed, you can run ```./convert.sh``` to generate the page PDF's followed by the following ghostscript command: ```gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=diceware.pdf page-*.pdf```