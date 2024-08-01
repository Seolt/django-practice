import os
import re


def changeStatic(html_link, output_link):
    with open(html_link, 'r', encoding='utf-8') as f:
        html_code = f.read()

    html_code = ('{% load static %}\n') + html_code
    results = re.sub("'", '"', html_code)  # Change ' to "

    # Exclude hrefs that start with http or https

    results = re.sub(r'href="(?!http)([^"]+?)(?<!\.html)(?<!#.?)"', r'href="{% static "\1" %}"', results)
    results = re.sub(r'src="(?!http)([^"]+?)(?<!\.html)(?<!#.?)"', r'src="{% static "\1" %}"', results)
    results = re.sub(r'url\(([^)]+)\)', r'url("{% static "\1" %}")', results)
    results = re.sub(r'href="([^"]+)\.html"', r'href="/\1"', results)
    with open(output_link, 'w', encoding='utf-8') as f2:
        f2.write(results)


folder_path = 'C:/Users/USER/source/repos/Eproject/Wendy/templates/Wendy'
file_extension = '.html'  # File extension you want to read

# Open all files in a folder
for filename in os.listdir(folder_path):
    if filename.endswith(file_extension):
        file_path = os.path.join(folder_path, filename)
        changeStatic(file_path, file_path)