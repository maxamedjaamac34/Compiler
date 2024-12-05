class Token:
    def __init__(self, token_type, token_value):
        self.tokenType = token_type
        self.tokenValue = token_value
class CompilationEngine:
    def __init__(self, tokens):
        """
        Initializes the compilation engine with a stream of tokens.
        """
        self.tokens = tokens  
        self.current_index = 0
        self.class_name = None
        self.output = []
        self.indent_level = 0

    def current_token(self):
        #This one should return the current token, unless we have reached the end of the file
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def advance(self):
        #advance moves to the next token, unless we have reached the end of the file.
        if self.current_index < len(self.tokens):
            self.current_index += 1
    def write_tag(self, tag, value=None):
        """Writes an opening or self-closing XML tag."""
        indent = "  " * self.indent_level
        if value: #if we have a value, then it is a non terminal rule, and we need to close it
            self.output.append(f"{indent}<{tag}> {value} </{tag}>")
        else: #if its a non terminal we need to indent its elements by 1
            self.output.append(f"{indent}<{tag}>")
            self.indent_level += 1

    def close_tag(self, tag):
        """Writes a closing XML tag."""
        self.indent_level -= 1 #once we have reached the end of that block, we need to indent one step back, write a closing tag and proceed from there
        indent = "  " * self.indent_level
        self.output.append(f"{indent}</{tag}>")

    def compile_class(self):
        """
        Compiles a Jack class:
        class : 'class' className '{' classVarDec* subroutineDec* '}'
        """
        token = self.current_token()
        self.write_tag("class")

        # Check for 'class' keyword
        if not (token and token.tokenType == "keyword" and token.tokenValue == "class"):
            raise SyntaxError("Expected 'class' keyword at the beginning of the class definition.")
        self.write_tag("keyword", token.tokenValue)  # <keyword> class </keyword>
        self.advance()

        # Check for class name (identifier)
        token = self.current_token()
        if not (token and token.tokenType == "identifier"):
            raise SyntaxError("Expected class name after 'class' keyword.")
        self.write_tag("identifier", token.tokenValue)  # <identifier> ClassName </identifier>
        self.class_name = token.tokenValue
        self.advance()

        # Check for '{' symbol
        token = self.current_token()
        if not (token and token.tokenType == "symbol" and token.tokenValue == "{"):
            raise SyntaxError("Expected '{' after class name.")
        self.write_tag("symbol", token.tokenValue)  # <symbol> { </symbol>
        self.advance()

        # Handle class variable declarations (classVarDec)
        token = self.current_token()
        while token and token.tokenValue in ("static", "field"):
            self.compile_class_var_dec()
            token = self.current_token()

        # Handle subroutine declarations (subroutineDec)
        while token and token.tokenValue in ("constructor", "function", "method"):
            self.compile_subroutine()
            token = self.current_token()

        # Check for closing '}' symbol
        if not (token and token.tokenType == "symbol" and token.tokenValue == "}"):
            raise SyntaxError("Expected '}' at the end of the class definition.")
        self.write_tag("symbol", token.tokenValue)  # <symbol> } </symbol>
        self.advance()

        self.close_tag("class")

    def compile_class_var_dec(self):
            
        """
        Compiles class variable declarations:
        classVarDec : ('static' | 'field') type varName (',' varName)* ';'
        """
        self.write_tag("classVarDec")  # Opening <classVarDec> tag

        # 'static' or 'field'
        token = self.current_token()
        if not (token and token.tokenValue in ("static", "field")):
            raise SyntaxError("Expected 'static' or 'field' for class variable declaration.")
        self.write_tag("keyword", token.tokenValue)
        self.advance()

        # Variable type
        token = self.current_token()
        if not (token and (token.tokenType == "keyword" or token.tokenType == "identifier")):
            raise SyntaxError("Expected type for class variable.")
        self.write_tag("keyword", token.tokenValue)  # Type (int, boolean, etc.)
        self.advance()

        # Variable names
        while True:
            # Variable name
            token = self.current_token()
            if not (token and token.tokenType == "identifier"):
                raise SyntaxError("Expected variable name.")
            self.write_tag("identifier", token.tokenValue)  # Variable name
            self.advance()

            # Handle ',' or ';'
            token = self.current_token()
            if token and token.tokenValue == ",":
                self.write_tag("symbol", token.tokenValue)  # Comma
                self.advance()  # Continue to the next variable
            elif token and token.tokenValue == ";":
                self.write_tag("symbol", token.tokenValue)  # Semicolon
                self.advance()  # End of declaration
                break
            else:
                raise SyntaxError("Expected ',' or ';' after variable name.")

        self.close_tag("classVarDec")  # Closing </classVarDec> tag


    def compile_subroutine(self):
        """
        Compiles subroutine definitions:
        subroutineDec : ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        """
        self.write_tag("subroutineDec")  # Opening <subroutineDec> tag

        # 'constructor', 'function', or 'method'
        token = self.current_token()
        if not (token and token.tokenValue in ("constructor", "function", "method")):
            raise SyntaxError("Expected 'constructor', 'function', or 'method'.")
        self.write_tag("keyword", token.tokenValue)
        self.advance()

        # Return type ('void' or type)
        token = self.current_token()
        if not (token and (token.tokenType == "keyword" or token.tokenType == "identifier")):
            raise SyntaxError("Expected return type for subroutine.")
        self.write_tag("keyword", token.tokenValue)
        self.advance()

        # Subroutine name (identifier)
        token = self.current_token()
        if not (token and token.tokenType == "identifier"):
            raise SyntaxError("Expected subroutine name.")
        self.write_tag("identifier", token.tokenValue)
        self.advance()

        # Parameter list
        token = self.current_token()
        if not (token and token.tokenValue == "("):
            raise SyntaxError("Expected '(' before parameter list.")
        self.write_tag("symbol", token.tokenValue)  # Opening '('
        self.advance()
        self.compile_parameter_list()
        token = self.current_token()
        if not (token and token.tokenValue == ")"):
            raise SyntaxError("Expected ')' after parameter list.")
        self.write_tag("symbol", token.tokenValue)  # Closing ')'
        self.advance()

        # Subroutine body
        self.write_tag("subroutineBody")  # Opening <subroutineBody> tag
        token = self.current_token()
        if not (token and token.tokenValue == "{"):
            raise SyntaxError("Expected '{' at the beginning of subroutine body.")
        self.write_tag("symbol", token.tokenValue)  # Opening '{'
        self.advance()

        # Variable declarations
        token = self.current_token()
        while token and token.tokenValue == "var":
            self.compile_var_dec()
            token = self.current_token()

        # Statements
        self.compile_statements()

        # Closing '}'
        token = self.current_token()
        if not (token and token.tokenValue == "}"):
            raise SyntaxError("Expected '}' at the end of subroutine body.")
        self.write_tag("symbol", token.tokenValue)  # Closing '}'
        self.advance()

        self.close_tag("subroutineBody")  # Closing </subroutineBody> tag
        self.close_tag("subroutineDec")  # Closing </subroutineDec> tag


    def compile_parameter_list(self):
        """
        Compiles the parameter list of a subroutine.
        parameterList : ((type varName) (',' type varName)*)?
        """
        self.write_tag("parameterList")  # Opening <parameterList> tag

        token = self.current_token()
        while token and token.tokenValue != ")":
            # Parameter type
            if not (token and (token.tokenType == "keyword" or token.tokenType == "identifier")):
                raise SyntaxError("Expected parameter type.")
            self.write_tag("keyword", token.tokenValue)  # Write parameter type
            self.advance()

            # Parameter name
            token = self.current_token()
            if not (token and token.tokenType == "identifier"):
                raise SyntaxError("Expected parameter name.")
            self.write_tag("identifier", token.tokenValue)  # Write parameter name
            self.advance()

            # Check for a comma or end of parameter list
            token = self.current_token()
            if token and token.tokenValue == ",":
                self.write_tag("symbol", token.tokenValue)  # Write comma
                self.advance()
                token = self.current_token()
            elif token and token.tokenValue == ")":
                break
            else:
                raise SyntaxError("Expected ',' or ')' in parameter list.")

        self.close_tag("parameterList")  # Closing </parameterList> tag


    def compile_var_dec(self):
        """
        Compiles variable declarations:
        varDec : 'var' type varName (',' varName)* ';'
        """
        self.write_tag("varDec")  # Opening <varDec> tag

        # 'var'
        token = self.current_token()
        if not (token and token.tokenValue == "var"):
            raise SyntaxError("Expected 'var' for variable declaration.")
        self.write_tag("keyword", token.tokenValue)
        self.advance()

        # Variable type
        token = self.current_token()
        if not (token and (token.tokenType == "keyword" or token.tokenType == "identifier")):
            raise SyntaxError("Expected type for variable.")
        self.write_tag("keyword", token.tokenValue)  # Write variable type
        self.advance()

        # Variable names
        while True:
            token = self.current_token()
            if not (token and token.tokenType == "identifier"):
                raise SyntaxError("Expected variable name.")
            self.write_tag("identifier", token.tokenValue)  # Write variable name
            self.advance()

            # Check for ',' or ';'
            token = self.current_token()
            if token and token.tokenValue == ",":
                self.write_tag("symbol", token.tokenValue)  # Write comma
                self.advance()
            elif token and token.tokenValue == ";":
                self.write_tag("symbol", token.tokenValue)  # Write semicolon
                self.advance()
                break
            else:
                raise SyntaxError("Expected ',' or ';' after variable name.")

        self.close_tag("varDec")  # Closing </varDec> tag

    def compile_statements(self):
        """
        Compiles a sequence of statements:
        statements : statement*
        """
        self.write_tag("statements")  # Opening <statements> tag

        token = self.current_token()
        while token and token.tokenValue in ("let", "if", "while", "do", "return"):
            if token.tokenValue == "let":
                self.compile_let_statement()
            elif token.tokenValue == "if":
                self.compile_if_statement()
            elif token.tokenValue == "while":
                self.compile_while_statement()
            elif token.tokenValue == "do":
                self.compile_do_statement()
            elif token.tokenValue == "return":
                self.compile_return_statement()
            token = self.current_token()

        self.close_tag("statements")  # Closing </statements> tag


    def compile_let_statement(self):
        """
        Compiles a Jack "let" statement:
        letStatement : 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self.write_tag("letStatement")  # Opening <letStatement> tag

        # 'let'
        token = self.current_token()
        if not (token and token.tokenValue == "let"):
            raise SyntaxError("Expected 'let' at the beginning of let statement.")
        self.write_tag("keyword", token.tokenValue)  # Write 'let'
        self.advance()

        # Variable name
        token = self.current_token()
        if not (token and token.tokenType == "identifier"):
            raise SyntaxError("Expected variable name in let statement.")
        self.write_tag("identifier", token.tokenValue)  # Write variable name
        self.advance()

        # Optional array indexing
        if self.current_token().tokenValue == "[":
            self.write_tag("symbol", "[")  # Write '['
            self.advance()
            self.compile_expression()
            if not (self.current_token().tokenValue == "]"):
                raise SyntaxError("Expected ']' after array indexing.")
            self.write_tag("symbol", "]")  # Write ']'
            self.advance()

        # Assignment operator '='
        if not (self.current_token().tokenValue == "="):
            raise SyntaxError("Expected '=' in let statement.")
        self.write_tag("symbol", "=")  # Write '='
        self.advance()

        # Expression
        self.compile_expression()

        # Semicolon ';'
        if not (self.current_token().tokenValue == ";"):
            raise SyntaxError("Expected ';' at the end of let statement.")
        self.write_tag("symbol", ";")  # Write ';'
        self.advance()

        self.close_tag("letStatement")  # Closing </letStatement> tag


    def compile_if_statement(self):
        """
        Compiles a Jack "if" statement:
        ifStatement : 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        self.write_tag("ifStatement")  # Opening <ifStatement> tag

        # 'if'
        token = self.current_token()
        if not (token and token.tokenValue == "if"):
            raise SyntaxError("Expected 'if' at the beginning of if statement.")
        self.write_tag("keyword", token.tokenValue)  # Write 'if'
        self.advance()

        # '('
        token = self.current_token()
        if not (token and token.tokenValue == "("):
            raise SyntaxError("Expected '(' after 'if'.")
        self.write_tag("symbol", token.tokenValue)  # Write '('
        self.advance()

        # Condition (expression)
        self.compile_expression()

        # ')'
        token = self.current_token()
        if not (token and token.tokenValue == ")"):
            raise SyntaxError("Expected ')' after if condition.")
        self.write_tag("symbol", token.tokenValue)  # Write ')'
        self.advance()

        # '{'
        token = self.current_token()
        if not (token and token.tokenValue == "{"):
            raise SyntaxError("Expected '{' for if block.")
        self.write_tag("symbol", token.tokenValue)  # Write '{'
        self.advance()

        # Statements in the true block
        self.compile_statements()

        # '}'
        token = self.current_token()
        if not (token and token.tokenValue == "}"):
            raise SyntaxError("Expected '}' at the end of if block.")
        self.write_tag("symbol", token.tokenValue)  # Write '}'
        self.advance()

        # Optional 'else' block
        token = self.current_token()
        if token and token.tokenValue == "else":
            self.write_tag("keyword", token.tokenValue)  # Write 'else'
            self.advance()

            # '{'
            token = self.current_token()
            if not (token and token.tokenValue == "{"):
                raise SyntaxError("Expected '{' for else block.")
            self.write_tag("symbol", token.tokenValue)  # Write '{'
            self.advance()

            # Statements in the else block
            self.compile_statements()

            # '}'
            token = self.current_token()
            if not (token and token.tokenValue == "}"):
                raise SyntaxError("Expected '}' at the end of else block.")
            self.write_tag("symbol", token.tokenValue)  # Write '}'
            self.advance()

        self.close_tag("ifStatement")  # Closing </ifStatement> tag


    def compile_while_statement(self):
        """
        Compiles a Jack "while" statement:
        whileStatement : 'while' '(' expression ')' '{' statements '}'
        """
        # Open the whileStatement tag
        self.write_tag("whileStatement")

        token = self.current_token()
        if not (token and token.tokenValue == "while"):
            raise SyntaxError("Expected 'while' at the beginning of while statement.")
        self.write_tag("keyword", "while")
        self.advance()

        # Open condition parenthesis
        token = self.current_token()
        if not (token and token.tokenValue == "("):
            raise SyntaxError("Expected '(' after 'while'.")
        self.write_tag("symbol", "(")
        self.advance()

        # Compile the condition expression
        self.compile_expression()

        # Close condition parenthesis
        token = self.current_token()
        if not (token and token.tokenValue == ")"):
            raise SyntaxError("Expected ')' after while condition.")
        self.write_tag("symbol", ")")
        self.advance()

        # Open loop block
        token = self.current_token()
        if not (token and token.tokenValue == "{"):
            raise SyntaxError("Expected '{' for while block.")
        self.write_tag("symbol", "{")
        self.advance()

        # Compile statements within the block
        self.compile_statements()

        # Close loop block
        token = self.current_token()
        if not (token and token.tokenValue == "}"):
            raise SyntaxError("Expected '}' at the end of while block.")
        self.write_tag("symbol", "}")
        self.advance()

        # Close the whileStatement tag
        self.close_tag("whileStatement")


    def compile_do_statement(self):
        """
        Compiles a Jack "do" statement:
        doStatement : 'do' subroutineCall ';'
        """
        # Open the doStatement tag
        self.write_tag("doStatement")

        # 'do' keyword
        token = self.current_token()
        if not (token and token.tokenValue == "do"):
            raise SyntaxError("Expected 'do' at the beginning of do statement.")
        self.write_tag("keyword", "do")
        self.advance()

        # Compile the subroutine call
        self.compile_subroutine_call()

        # Semicolon ';'
        token = self.current_token()
        if not (token and token.tokenValue == ";"):
            raise SyntaxError("Expected ';' at the end of do statement.")
        self.write_tag("symbol", ";")
        self.advance()

        # Close the doStatement tag
        self.close_tag("doStatement")


    def compile_return_statement(self):
        """
        Compiles a Jack "return" statement:
        returnStatement : 'return' expression? ';'
        """
        # Open the returnStatement tag
        self.write_tag("returnStatement")

        # 'return' keyword
        token = self.current_token()
        if not (token and token.tokenValue == "return"):
            raise SyntaxError("Expected 'return' at the beginning of return statement.")
        self.write_tag("keyword", "return")
        self.advance()

        # Optional expression
        if self.current_token() and self.current_token().tokenValue != ";":
            self.compile_expression()

        # Semicolon ';'
        token = self.current_token()
        if not (token and token.tokenValue == ";"):
            raise SyntaxError("Expected ';' at the end of return statement.")
        self.write_tag("symbol", ";")
        self.advance()

        # Close the returnStatement tag
        self.close_tag("returnStatement")

    def compile_expression(self):
        """
        Compiles a Jack expression:
        expression : term (op term)*
        """
        self.write_tag("expression")
        self.compile_term()

        while self.current_token() and self.unescape_symbol(self.current_token().tokenValue) in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            operator = self.unescape_symbol(self.current_token().tokenValue)
            self.write_tag("symbol", self.escape_symbol(operator))
            self.advance()
            self.compile_term()

        self.close_tag("expression")
    def escape_symbol(self, symbol):
        """
        Escapes special XML characters into their escaped forms.
        """
        symbol_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
        }
        return symbol_map.get(symbol, symbol)



    def unescape_symbol(self, symbol):
        """
        Unescapes special XML characters into their original forms.
        """
        symbol_map = {
            "&lt;": "<",
            "&gt;": ">",
            "&amp;": "&",
        }
        return symbol_map.get(symbol, symbol)
    def compile_term(self):
        """
        Compiles a Jack term:
        term : integerConstant | stringConstant | keywordConstant |
            varName | varName '[' expression ']' |
            subroutineCall | '(' expression ')' | unaryOp term
        """
        # Open the term tag
        self.write_tag("term")

        token = self.current_token()

        if token is None:
            raise SyntaxError("Unexpected end of input while parsing term.")

        if token.tokenType == "integerConstant":
            self.write_tag("integerConstant", token.tokenValue)
            self.advance()
        elif token.tokenType == "stringConstant":
            self.write_tag("stringConstant", token.tokenValue)
            self.advance()
        elif token.tokenType == "keyword" and token.tokenValue in ("true", "false", "null", "this"):
            self.write_tag("keyword", token.tokenValue)
            self.advance()
        elif token.tokenType == "symbol" and token.tokenValue == "(":
            # Parentheses expression
            self.write_tag("symbol", token.tokenValue)
            self.advance()  # "("
            self.compile_expression()
            if not (self.current_token() and self.current_token().tokenValue == ")"):
                raise SyntaxError(f"Expected ')' after expression. Found: {self.current_token().tokenValue if self.current_token() else 'None'}")
            self.write_tag("symbol", self.current_token().tokenValue)
            self.advance()  # ")"
        elif token.tokenType == "symbol" and token.tokenValue in ("-", "~"):  # Unary operation
            operator = token.tokenValue
            self.write_tag("symbol", operator)
            self.advance()
            self.compile_term()
        else:  # Handle varName, array indexing, or subroutine call
            if token.tokenType != "identifier":
                raise SyntaxError(f"Expected identifier, found {token.tokenValue}")
            identifier = token.tokenValue
            self.write_tag("identifier", identifier)
            self.advance()

            if self.current_token() and self.current_token().tokenValue == "[":
                # Array indexing
                self.write_tag("symbol", self.current_token().tokenValue)
                self.advance()  # "["
                self.compile_expression()
                if not (self.current_token() and self.current_token().tokenValue == "]"):
                    raise SyntaxError("Expected ']' after array index expression.")
                self.write_tag("symbol", self.current_token().tokenValue)
                self.advance()  # "]"
            elif self.current_token() and self.current_token().tokenValue in ("(", "."):
                # Subroutine call
                self.compile_subroutine_call(identifier)

        # Close the term tag
        self.close_tag("term")


    def compile_subroutine_call(self, identifier=None):
        """
        Compiles a Jack subroutine call:
        subroutineCall : subroutineName '(' expressionList ')' |
                        (className | varName) '.' subroutineName '(' expressionList ')'
        """
        # Open the subroutineCall tag
        #self.write_tag("subroutineCall") we dont need the subroutine call tag

        if identifier is None:
            if self.current_token().tokenType != "identifier":
                raise SyntaxError("Expected subroutine name or identifier.")
            identifier = self.current_token().tokenValue
            self.write_tag("identifier", identifier)
            self.advance()

        if self.current_token() and self.current_token().tokenValue == ".":
            # Method or function call
            self.write_tag("symbol", ".")
            self.advance()  # "."
            if self.current_token().tokenType != "identifier":
                raise SyntaxError("Expected subroutine name after '.'.")
            subroutine_name = self.current_token().tokenValue
            self.write_tag("identifier", subroutine_name)
            self.advance()
            identifier = f"{identifier}.{subroutine_name}"

        if not (self.current_token() and self.current_token().tokenValue == "("):
            raise SyntaxError("Expected '(' for subroutine call.")
        self.write_tag("symbol", "(")
        self.advance()  # "("

        # Compile the expression list
        self.compile_expression_list()

        if not (self.current_token() and self.current_token().tokenValue == ")"):
            raise SyntaxError("Expected ')' after subroutine call.")
        self.write_tag("symbol", ")")
        self.advance()  # ")"

        # Close the subroutineCall tag
        #self.close_tag("subroutineCall")

    def compile_expression_list(self):
        """
        Compiles a list of expressions:
        expressionList : (expression (',' expression)*)?
        Returns:
            int: The number of expressions compiled.
        """
        # Open the expressionList tag
        self.write_tag("expressionList")

        count = 0

        if self.current_token() and self.current_token().tokenValue != ")":
            self.compile_expression()
            count += 1

            while self.current_token() and self.current_token().tokenValue == ",":
                self.write_tag("symbol", ",")
                self.advance()  # ","
                self.compile_expression()
                count += 1

        # Close the expressionList tag
        self.close_tag("expressionList")

        return count



        

def parse_tokenized_xml(file_path):
    """
    Reads a tokenized XML file line by line and creates a list of Token objects.
    """
    tokens = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("<") and line.endswith(">") and not line.startswith("<tokens"):
                # Extract token type
                token_type_start = line.find("<") + 1
                token_type_end = line.find(">")
                token_type = line[token_type_start:token_type_end]

                # Extract token value
                token_value_start = token_type_end + 1
                token_value_end = line.find(f"</{token_type}>")
                token_value = line[token_value_start:token_value_end].strip()

                # Create a Token object
                tokens.append(Token(token_type, token_value))
    return tokens


tokenized_file_path = "/Users/stephen/Documents/GitHub/Compiler/Compiler-testing/SquareT.xml"
tokens = parse_tokenized_xml(tokenized_file_path)
compilation_engine = CompilationEngine(tokens)
compilation_engine.compile_class()

#Save to output file
output_file_path = "/Users/stephen/Documents/GitHub/Compiler/Compiler-testing/Squareoutput.xml"
with open(output_file_path, "w") as file:
    file.write("\n".join(compilation_engine.output))