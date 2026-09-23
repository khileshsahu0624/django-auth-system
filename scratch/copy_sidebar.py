import re

with open('students/templates/students/student_list.html', 'r', encoding='utf-8') as f:
    student_html = f.read()

sidebar_match = re.search(r'(<aside class="sidebar" id="sidebar">.*?</aside>)', student_html, re.DOTALL)
if not sidebar_match:
    print('Sidebar not found in student_list.html')
    exit(1)
sidebar_html = sidebar_match.group(1)

with open('user_management/templates/user_management/user_list.html', 'r', encoding='utf-8') as f:
    user_html = f.read()

user_html_new = re.sub(r'<aside class="sidebar" id="sidebar">.*?</aside>', sidebar_html, user_html, flags=re.DOTALL)

with open('user_management/templates/user_management/user_list.html', 'w', encoding='utf-8') as f:
    f.write(user_html_new)
print('Sidebar copied successfully.')
