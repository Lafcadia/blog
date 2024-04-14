import sys
from heic_image_converter.Converter import Converter

# EX: > python [path/to/convert.py](0) [path/to/sourceDir](1) --to(2) [saveAs](3) --dest(4) [path/to/saveDir](5) -del
if __name__ == "__main__":
	ImgConverter = Converter(sys.argv[1:])
	ImgConverter.convert_files()