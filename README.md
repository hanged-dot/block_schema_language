# Block schema language

This project is dedicated to creating a simple language dedicated to creating block schemas. The language uses the graphviz .dot language for a base model to create images of schemas.

## Usage 

1. Create a text file, defining your schema using the grammar provided. 
2. Run the following command:
``` python main.py -i="your_file_with_schema.block" -o="output_file_name.dot"```.
It is important that the output file has the .dot file extension.
3. Run the graphviz command ```dot -Tpng output_file_name.dot -o output_file_name.png ```. You can specify any other picture format that you may need by changing the second file extension and adding it after the ```-T``` parameter. 

The final schema should be now in this directory. It is recommended that you use seperate subdirectories for each of the files.

Feel free to use examples in ```block``` directory.