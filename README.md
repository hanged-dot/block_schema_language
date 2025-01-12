# Block schema language

This project is dedicated to creating a simple language dedicated to creating block schemas. The language uses the Graphviz dot language for a base model to create images of schemas.

## Requirements

Make sure that you have a Graphviz program installed and `dot` is in your PATH. Install Python version above 3.9 and python dependencies listed in `requirents.txt`

## Usage

1. Create a text file, defining your schema using the grammar provided.
2. Run the following command:
` python main.py -i="your_file_with_schema.block" `.

If block schema was defined correctly, the final schema should be now in `png` directory. The image should also show up on your screen.

Feel free to use examples in `block` directory. You can also look at a `.dot` file generated in the process.
