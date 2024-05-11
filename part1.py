# Open the original file
with open("finalv1.txt", "r") as file:
    lines = file.readlines()

# Remove comment lines, "of an expression", and extra spaces
cleaned_lines = []
for line in lines:
    # Remove comments
    if "//" in line:
        line = line[:line.index("//")].strip()
    # Remove "of an expression"
    if "of an expression" in line:
        continue
    # Remove extra spaces and add one space before and after each token
    cleaned_line = " ".join(line.split())
    # Skip empty lines
    if cleaned_line:
        cleaned_lines.append(cleaned_line)

# Write the cleaned lines to the new file
with open("final24.txt", "w") as file:
    for line in cleaned_lines:
        file.write(line + "\n")
