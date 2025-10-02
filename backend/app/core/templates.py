from fastapi.templating import Jinja2Templates

# Tell FastAPI where templates live (inside app/templates/)
templates = Jinja2Templates(directory="templates")
