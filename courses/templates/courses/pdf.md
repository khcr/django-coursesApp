---
title: {{ course.name }}
author: {{ course.author.first_name }} {{ course.author.last_name}}
date: {{ course.created_at | date:"d F Y" }}
---

*Note: Il se peut que la mise en forme diffère légèrement de la version en ligne.*

{{ course.description }}

{% for page in course.pages.all %}

## {{ page.name }}

{% for section in page.sections.all %}

### {{ section.name }}

{{ section.markdown_content }}

{% endfor %}
{% endfor %}