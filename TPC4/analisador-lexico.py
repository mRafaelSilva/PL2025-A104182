import re
import sys

def tokenize_query(query):
    token_specification = [
        ("SELECT", r'select'),
        ("VAR", r'\?[a-zA-Z_][a-zA-Z0-9_]*'),
        ("WHERE", r'where'),
        ("LIMIT", r'LIMIT'),
        ("NUMBER", r'\d+'),
        ("STRING", r'".*?"(@[a-zA-Z]+)?'),
        ("URI", r'[a-zA-Z]+:[a-zA-Z]+'),
        ("SYMBOL", r'[{}:.]'),
        ("WHITESPACE", r'\s+'),
        ("ERROR", r'.')
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
    tokens = [(match.lastgroup, match.group()) for match in re.finditer(token_regex, query, re.IGNORECASE) if match.lastgroup != "WHITESPACE"]
    
    return tokens

if __name__ == "__main__":
    query = '''select ?nome ?desc where {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?w dbo:artist ?s.
        ?w foaf:name ?nome.
        ?w dbo:abstract ?desc
    } LIMIT 1000'''
    
    tokens = tokenize_query(query)
    for token in tokens:
        print(token)