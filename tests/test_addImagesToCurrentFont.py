import sys, os

# add scripts dir to sys.path
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'LP_addImagesToCurrentFont'))

sys.path.append(script_dir)

from LP_addImagesToCurrentFont import parseFiles
import unittest



class TestParseDirectory(unittest.TestCase):

    fullPath = "/home/robo/images/"

    def test_itReturnsADictionary(self):
        result = parseFiles(self.fullPath, [])
        self.assertTrue( isinstance(result, dict))



    def test_itFiltersInvalidFileExtensions(self):
    	fileList = ["lc-b.txt",
    				"lc-a.doc",
    				"lc-a.ai"]
    	result = parseFiles(self.fullPath, fileList)
    	self.assertEquals(len(result), 0)


    def test_itHandlesNumbers(self):
        fileList = ["num-0.png",
                    "num-10.png",
                    "num-zero.png",
                    "num-FIVE.png",
                    "num-four.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"zero": "/home/robo/images/num-zero.png",
                                   "four": "/home/robo/images/num-four.png"})
    
    # not strict on two letter combinations
    def test_itHandlesLowerCaseLetters(self):
        fileList = ["lc-b.png",
                    "lC-A.png",
                    "lc-invalidglyphname.png",
                    "lc-a-acute.png",
                    "lc-ae.tif",
                    "lc-ui.tif"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"b": "/home/robo/images/lc-b.png",
                                   "aacute": "/home/robo/images/lc-a-acute.png",
                                   "ae": "/home/robo/images/lc-ae.tif",
                                   "ui": "/home/robo/images/lc-ui.tif"})

    # not strict on two letter combinations
    def test_itHandlesUpperCaseLetters(self):
        fileList = ["UC-B.png",
                    "uC-C.png",
                    "UC-INVALIDGLYPHNAME.png",
                    "UC-A-acute.png",
                    "UC-AE.tif"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"B": "/home/robo/images/UC-B.png",
                                   "Aacute": "/home/robo/images/UC-A-acute.png",
                                   "AE": "/home/robo/images/UC-AE.tif"})


    # handling of punctuation can lead to introduction of non standard glyph names
    def test_itHandlesEverythingElse(self):
        fileList = ["a.tif",
                    "ampersand.png",
                    "bulubu.png",
                    "Dswash.png"]
        result = parseFiles(self.fullPath, fileList)
        self.assertEquals(result, {"ampersand": "/home/robo/images/ampersand.png",
                                   "bulubu": "/home/robo/images/bulubu.png",
                                   "Dswash": "/home/robo/images/Dswash.png" })



def main():
    unittest.main()

if __name__ == '__main__':
    main()