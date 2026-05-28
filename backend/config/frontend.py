"""Serve static HTML/CSS/JS from ../frontend (same origin as API)."""
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.views.static import serve

FRONTEND_ROOT = (Path(settings.BASE_DIR).parent / 'frontend').resolve()


def serve_frontend(request, path=''):
    """Safe file serving for multi-page static site."""
    path = (path or '').strip() or 'index.html'
    if '..' in path or path.startswith(('/', '\\')):
        raise Http404()
    target = (FRONTEND_ROOT / path).resolve()
    try:
        target.relative_to(FRONTEND_ROOT)
    except ValueError:
        raise Http404()
    if not target.exists() or target.is_dir():
        raise Http404()
    return serve(request, path, document_root=str(FRONTEND_ROOT))
