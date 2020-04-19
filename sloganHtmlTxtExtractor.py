filename = "./rawHtml.txt"

def containsSlogan(line):
    return "<span class=\"slogan\">" in line

with open(filename) as f:
    lines = f.read().splitlines()

filtered = filter(containsSlogan, lines)

slogs = []

for s in filtered: 
    startIndex = s.index("<span class=\"slogan\">") + 21
    endIndex = len(s)-1
    if("<br>" in str(s)):
        endIndex = s.index("<br>")
    elif("</" in str(s)):
        endIndex = s.index("</")
    slogs.append(s[startIndex:endIndex].encode('UTF-8'))

print(slogs)