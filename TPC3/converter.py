import re

def processa_lista(match):
    items = re.sub(r'\n?(\d+)\. (.+)', r'<li>\2</li>\n', match.group(0))
    return f'<ol>\n{items}</ol>'

def converter(text):
    text = re.sub(r'^### (.+)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    text = re.sub(r'(?:^|\n)(\d+\. .+)(?:\n\d+\. .+)*', processa_lista, text)
    
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', text)
    
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    return text


print("Escreve o texto Markdown:")
lines = []
while True:
    line = input()
    if line == "": 
        break
    lines.append(line)

user_input = "\n".join(lines)
print("\nOutput HTML:")
print(converter(user_input))
