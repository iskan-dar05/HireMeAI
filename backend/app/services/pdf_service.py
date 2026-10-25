from jinja2 import Environment, BaseLoader, select_autoescape
from weasyprint import HTML
from app.models.cv import CV
from app.models.cv_design import CVDesign

TEMPLATE = r"""
<!doctype html><html><head><meta charset="utf-8">
<style>
@page { size: A4; margin: 16mm; }
* { box-sizing: border-box; }
body { font-family: Arial, sans-serif; color: #263238; font-size: 10pt; line-height: 1.4; }
h1 { margin: 0 0 4px; font-size: 24pt; color: {{ color }}; }
h2 { font-size: 12pt; margin: 16px 0 5px; border-bottom: 1px solid #d9e0e5; padding-bottom: 3px; color: {{ color }}; }
p { margin: 3px 0; } ul { margin: 4px 0; padding-left: 18px; }
.small { color: #5b6870; font-size: 9pt; }
</style></head><body>
{% set personal = content.get('personal_info', {}) %}
<h1>{{ personal.get('name', 'Your Name') }}</h1>
<p><strong>{{ personal.get('headline', '') }}</strong></p>
<p class="small">{{ personal.get('email', '') }} {% if personal.get('phone') %} · {{ personal.get('phone') }}{% endif %} {% if personal.get('location') %} · {{ personal.get('location') }}{% endif %}</p>
{% if personal.get('summary') %}<h2>Professional Summary</h2><p>{{ personal.get('summary') }}</p>{% endif %}
{% if content.get('skills') %}<h2>Skills</h2><p>{{ content.get('skills') | join(', ') }}</p>{% endif %}
{% if content.get('experience') %}<h2>Experience</h2>{% for item in content.get('experience', []) %}
<p><strong>{{ item.get('title', '') }}</strong> — {{ item.get('company', '') }} <span class="small">{{ item.get('dates', '') }}</span></p>
{% if item.get('description') %}<p>{{ item.get('description') }}</p>{% endif %}
{% if item.get('bullets') %}<ul>{% for bullet in item.get('bullets', []) %}<li>{{ bullet }}</li>{% endfor %}</ul>{% endif %}
{% endfor %}{% endif %}
{% if content.get('projects') %}<h2>Projects</h2>{% for item in content.get('projects', []) %}<p><strong>{{ item.get('name', '') }}</strong> — {{ item.get('description', '') }}</p>{% endfor %}{% endif %}
{% if content.get('education') %}<h2>Education</h2>{% for item in content.get('education', []) %}<p><strong>{{ item.get('degree', '') }}</strong> — {{ item.get('institution', '') }} <span class="small">{{ item.get('dates', '') }}</span></p>{% endfor %}{% endif %}
{% if content.get('certifications') %}<h2>Certifications</h2><ul>{% for item in content.get('certifications', []) %}<li>{{ item.get('name', item) }}</li>{% endfor %}</ul>{% endif %}
</body></html>
"""

def render_cv_pdf(cv: CV, design: CVDesign | None = None) -> bytes:
    # Starter renderer: use a validated subset of design tokens. Extend for multi-column templates.
    spec = (design.layout_spec if design else {}) or {}
    color = "#243447"
    try:
        candidate = spec.get("style", {}).get("heading_color", color)
        if isinstance(candidate, str) and len(candidate) in (4, 7) and candidate.startswith("#"):
            color = candidate
    except AttributeError:
        pass
    env = Environment(loader=BaseLoader(), autoescape=select_autoescape(["html", "xml"]))
    html = env.from_string(TEMPLATE).render(content=cv.content or {}, color=color)
    return HTML(string=html).write_pdf()
