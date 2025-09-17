from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def root_redirect(request):
    #redirect ai docs di swagger una volta effettuato il log in
    docs_url = reverse("swagger-ui")
    if request.user.is_authenticated:
        return redirect(docs_url)
    return redirect(f"{settings.LOGIN_URL}?next={docs_url}")

def logout_get(request):
    #logout via GET e redirect al login con ritorno ai docs
    logout(request)
    return redirect("/api/auth/session/login/?next=/swagger/docs/")