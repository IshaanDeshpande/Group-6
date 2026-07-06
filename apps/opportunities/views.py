from typing import TYPE_CHECKING

# Provide real imports to type checkers/IDEs, but fall back at runtime so the
# module can be imported in environments where Django or DRF aren't installed.
if TYPE_CHECKING:
    # type checkers and IDEs will use the real imports for intellisense
    from django.shortcuts import render  # type: ignore
    from rest_framework import viewsets  # type: ignore
else:
    try:
        from django.shortcuts import render
    except Exception:
        # Lightweight runtime fallback so import-time checks don't fail. If
        # render is actually called at runtime without Django installed this
        # will raise to indicate misconfiguration.
        def render(request, template_name, context=None, *args, **kwargs):
            raise RuntimeError("django.shortcuts.render is not available")

    try:
        from rest_framework import viewsets
    except Exception:
        # Minimal fallback so the module can be imported without rest_framework
        class _DummyViewsets:
            class ModelViewSet:  # type: ignore
                pass

        viewsets = _DummyViewsets


class OpportunityViewSet(viewsets.ModelViewSet):
    pass
