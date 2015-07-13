/**
 * Individual base pairs are rendered differently depending on the scale.
 * This enum & associated functions help track these transitions.
 * @flow
 */

var DisplayMode = {
  LOOSE: 1,   // Lots of space -- a big font is OK.
  TIGHT: 2,   // Letters need to be shrunk to fit.
  BLOCKS: 3,  // Change from letters to blocks of color
  HIDDEN: 4,

  getDisplayMode(pxPerLetter: number): number {
    if (pxPerLetter >= 25) {
      return DisplayMode.LOOSE;
    } else if (pxPerLetter >= 10) {
      return DisplayMode.TIGHT;
    } else if (pxPerLetter >= 1) {
      return DisplayMode.BLOCKS;
    } else {
      return DisplayMode.HIDDEN;
    }
  },

  toString(mode: number): string {
    if (mode == DisplayMode.LOOSE) {
      return 'loose';
    } else if (mode == DisplayMode.TIGHT) {
      return 'tight';
    } else if (mode == DisplayMode.BLOCKS) {
      return 'blocks';
    } else {
      return 'hidden';
    }
  },

  isText(mode: number): boolean {
    return (mode == DisplayMode.LOOSE || mode == DisplayMode.TIGHT);
  }
};

module.exports = DisplayMode;