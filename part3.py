class Translator:
    def __init__(self):
        self.code = []

    def add(self, line):
        self.code.append(line)

    def save(self):
        with open('./output/output.py', 'w') as file:
            file.writelines(f"{line}\n" for line in self.code)

    def display(self):
        print('\n'.join(self.code))

def convert_to_python(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Splitting the content into lines and stripping leading/trailing whitespace
    lines = [line.strip() for line in content.split('\n')]

    # Reformatting the lines with proper indentation
    formatted_content = []
    inside_main = False
    for line in lines:
        if line.startswith("program"):
            formatted_content.append("# Converted from final24.txt")
        elif line.startswith("begin"):
            formatted_content.append("def main():")
            inside_main = True
        elif line.startswith("end."):
            inside_main = False
        elif inside_main:
            if line.startswith("var"):
                line = line.replace("var", "").replace("integer", "").replace(";", "").strip()
                variables = [v.strip() for v in line.split(",")]
                for var in variables:
                    formatted_content.append(f"    {var} = None")
            elif line.startswith("write"):
                line = line.replace("write", "print").replace(";", "").replace("(", "(").replace(")", ")")
                formatted_content.append(f"    {line}")
            else:
                formatted_content.append(f"    {line.replace(';', '')}")

    # Adding the if __name__ block
    formatted_content.append("\nif __name__ == '__main__':\n    main()")

    # Writing the formatted content to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_content))

# Replace 'final24.txt' and 'output.py' with your file names
convert_to_python('final24.txt', 'output.py')
