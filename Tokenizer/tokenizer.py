import sys

# Define keywords and symbols for the language
KEYWORDS = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
SYMBOLS = {"{", "}", "(", ")", "[", "]", "+", "-", ".", ",", "*", "/", "&", "|", "<", ">", "~", ";", "="}

# List to store tokens
tokens = []

class Token:
    def __init__(self, line_no: int, column_no: int, token_type: str, token_value: str):
        self.lineNo = line_no
        self.columnNo = column_no
        self.tokenType = token_type
        self.tokenValue = token_value

    def __str__(self):
        return f"<{self.tokenType}> {self.tokenValue} </{self.tokenType}>"

def add_token(line_no, column_no, token_type, token_value):
    """Helper function to create a Token and add it to the tokens list."""
    tokens.append(Token(line_no, column_no, token_type, token_value))

def remove_comments(lines):
    """Remove comments from the given lines."""
    clean_lines = []
    inside_multiline_comment = False

    for line in lines:
        if inside_multiline_comment:
            end_comment_index = line.find("*/")
            if end_comment_index != -1:
                inside_multiline_comment = False
                line = line[end_comment_index + 2:]
            else:
                continue

        while "/*" in line:
            start_comment_index = line.find("/*")
            end_comment_index = line.find("*/", start_comment_index + 2)
            if end_comment_index != -1:
                line = line[:start_comment_index] + line[end_comment_index + 2:]
            else:
                line = line[:start_comment_index]
                inside_multiline_comment = True
                break

        if not inside_multiline_comment:
            single_comment_index = line.find("//")
            if single_comment_index != -1:
                line = line[:single_comment_index]

        clean_lines.append(line)

    return clean_lines

def un_string_line(line, line_no):
    i = 0
    while i < len(line):
        if line[i] == "\"":  # check for string constant
            opening_quote_index = i
            i += 1
            while i < len(line) and line[i] != "\"":
                i += 1
            if i < len(line):
                closing_quote_index = i
                string_constant = line[opening_quote_index:closing_quote_index + 1]
                add_token(line_no, opening_quote_index, "stringConstant", string_constant)
                line = line[:opening_quote_index] + " " * (closing_quote_index - opening_quote_index + 1) + line[closing_quote_index + 1:]
            else:
                raise ValueError("Unmatched quote in string constant")
        i += 1

    i = 0
    while i < len(line):
        if line[i].isspace():
            i += 1
            continue

        elif line[i].isdigit():  # check integer constants
            start_index = i
            while i < len(line) and line[i].isdigit():
                i += 1
            integer_constant = line[start_index:i]
            add_token(line_no, start_index, "integerConstant", integer_constant)

        elif line[i].isalpha() or line[i] == "_":  # check identifiers and keywords
            start_index = i
            while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                i += 1
            identifier = line[start_index:i]
            if identifier in KEYWORDS:
                add_token(line_no, start_index, "keyword", identifier)
            else:
                add_token(line_no, start_index, "identifier", identifier)

        elif line[i] in SYMBOLS:  # Detect symbols
            symbol = line[i]
            add_token(line_no, i, "symbol", symbol)
            i += 1

        else:
            i += 1

def write_tokens_to_xml(filename="tokenizedfile.xml"):
    with open(filename, "w") as file:
        file.write("<tokens>\n")
        for token in tokens:
            file.write(f"  {token}\n")
        file.write("</tokens>\n")

def main():
    # Check if the filename is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python tokenizer.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]

    try:
        # Open the input file and process each line
        with open(input_filename, "r") as file_input:
            code_lines = file_input.readlines()
            clean_lines = remove_comments(code_lines)
            for line_no, line in enumerate(clean_lines, start=1):
                un_string_line(line, line_no)

        # Write the tokens to the XML file
        write_tokens_to_xml()

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
