import argparse
from pathlib import Path
import subprocess
from PIL import Image
from os.path import abspath, dirname, join


from lexer_parser import run_main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Provide an input file with file containing block schema")
    parser.add_argument('-i','--input_file', type=str, help="Input file with raw text")
    args = parser.parse_args()
    file_name = Path(args.input_file).stem
    path = join(dirname(abspath(__file__)), "dot", f"{file_name}.dot")
    if run_main(args.input_file, path):
        path_2=join(dirname(abspath(__file__)), "png", f"{file_name}.png")
        subprocess.run(["dot", "-Tpng", path, "-o", path_2 ])
        with Image.open(path_2) as img:
            img.show()
    else: 
        print("Check exception")