import re
import os

student_list_path = 'students/templates/students/student_list.html'
user_list_path = 'user_management/templates/user_management/user_list.html'
base_path = 'students/templates/students/base.html'

with open(student_list_path, 'r', encoding='utf-8') as f:
    student_html = f.read()

with open(user_list_path, 'r', encoding='utf-8') as f:
    user_html = f.read()

# EXTRACT PARTS FROM STUDENT_LIST
# 1. Head (up to </head>)
head_match = re.search(r'(<!doctype html>\s*<html[^>]*>\s*<head>.*?</head>)', student_html, re.DOTALL | re.IGNORECASE)
head = head_match.group(1)

# Add title block inside head (replace existing title)
head = re.sub(r'<title>.*?</title>', '<title>{% block title %}Learnix LMS{% endblock %}</title>', head)
# Add extra_css block just before </head>
head = head.replace('</head>', '  {% block extra_css %}{% endblock %}\n</head>')

# 2. Body start up to Sidebar
body_start_match = re.search(r'(<body>\s*<div class="app">\s*<div class="sidebar-overlay"[^>]*></div>)', student_html, re.DOTALL)
body_start = body_start_match.group(1)

# 3. Sidebar
sidebar_match = re.search(r'(<aside class="sidebar"[^>]*>.*?</aside>)', student_html, re.DOTALL)
sidebar = sidebar_match.group(1)

# Modify sidebar active link based on a block or variable if possible.
# For simplicity, we can remove the 'active' class entirely from the base sidebar,
# or we can use django url resolving to conditionally add 'active'.
# Let's add {% if request.resolver_match.url_name == 'student_list' %} active {% endif %}
sidebar = sidebar.replace('class="nav-item active" href="{% url \'student_list\' %}"', 'class="nav-item {% if request.resolver_match.url_name == \'student_list\' %}active{% endif %}" href="{% url \'student_list\' %}"')
sidebar = sidebar.replace('class="nav-item" href="{% url \'users_roles\' %}"', 'class="nav-item {% if request.resolver_match.url_name == \'users_roles\' %}active{% endif %}" href="{% url \'users_roles\' %}"')

# 4. Main start and Topbar
topbar_match = re.search(r'(<div class="main">\s*<!-- TOP HEADER -->\s*<header class="topbar">.*?</header>)', student_html, re.DOTALL)
if not topbar_match:
    # try without comment
    topbar_match = re.search(r'(<div class="main">\s*<header class="topbar">.*?</header>)', student_html, re.DOTALL)
topbar = topbar_match.group(1)

# 5. Script block
script_match = re.search(r'(<script>.*?</script>\s*</body>\s*</html>)', student_html, re.DOTALL)
script = script_match.group(1)
# Add extra_js before </body>
script = script.replace('</body>', '{% block extra_js %}{% endblock %}\n</body>')

# Construct base.html
base_content = f"""{head}
{body_start}

<!-- ===================== SIDEBAR ===================== -->
{sidebar}

<!-- ===================== MAIN ===================== -->
{topbar}

<!-- CONTENT -->
<div class="content">
  {{% block content %}}
  {{% endblock %}}
</div>

</div>
</div>

{script}
"""

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)


# EXTRACT CONTENT FROM STUDENT_LIST
# Content starts after <div class="content"> and ends before script
content_match = re.search(r'<div class="content">(.*?)</div>\s*</div>\s*</div>\s*<script>', student_html, re.DOTALL)
if not content_match:
    # Let's try matching everything between <div class="content"> and the end of the divs
    content_match = re.search(r'<div class="content">(.*?)\s*</div>\s*</div>\s*</div>', student_html, re.DOTALL)

student_content = content_match.group(1).strip()

new_student_html = f"""{{% extends 'students/base.html' %}}

{{% block title %}}Super Admin · Dashboard{{% endblock %}}

{{% block content %}}
{student_content}
{{% endblock %}}
"""

with open(student_list_path, 'w', encoding='utf-8') as f:
    f.write(new_student_html)


# EXTRACT CONTENT FROM USER_LIST
# Since user_list.html has an exact copy of the layout (including <script>), we do the same
# We need to extract extra_css if any (none exist in user_list specifically, style is same)
# We extract content
user_content_match = re.search(r'<div class="content">(.*?)\s*</div>\s*</div>\s*</div>', user_html, re.DOTALL)
user_content = user_content_match.group(1).strip()

# We also need the userSearch script which was specific to user_list.html
# In user_list.html, the script is at the bottom. We only need the specific filterUsers logic.
user_script_match = re.search(r'const search=document\.getElementById.*?filterUsers\)\);\n}', user_html, re.DOTALL)
extra_js = ""
if user_script_match:
    extra_js = f"<script>\n{user_script_match.group(0)}\n</script>"
else:
    # Just grab all the script from user_list and subtract the common script parts
    # Or just extract the specific variables:
    user_script_match = re.search(r'(const search=document.*?});\n}', user_html, re.DOTALL)
    if user_script_match:
        extra_js = f"<script>\n{user_script_match.group(1)}\n</script>"

new_user_html = f"""{{% extends 'students/base.html' %}}

{{% block title %}}Super Admin · Users & Roles{{% endblock %}}

{{% block content %}}
{user_content}
{{% endblock %}}

{{% block extra_js %}}
{extra_js}
{{% endblock %}}
"""

with open(user_list_path, 'w', encoding='utf-8') as f:
    f.write(new_user_html)

print("Base, student_list, and user_list refactored successfully.")
