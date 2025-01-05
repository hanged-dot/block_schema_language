import argparse

from lexer_parser import run_main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Provide an input file with file containing block schema")
    parser.add_argument('-i','--input_file', type=str, help="Input file with raw text")
    parser.add_argument('-o', '--output_file', type=str, help="Output file to which schema drawing will be saved to")
    args = parser.parse_args()
    run_main(args.input_file, args.output_file)
    