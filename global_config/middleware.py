import re

# Match semplice per un JWT (3 parti base64url separate da ".")
_JWT_LIKE = re.compile(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')

class BearerTokenMiddleware:
    """
    Se arriva Authorization con un JWT senza prefisso),
    aggiunge 'Bearer ' così SimpleJWT lo accetta.
    Esempi accettati:
      - Authorization: <jwt>
      - Authorization: Bearer <jwt> 
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION")
        if auth:
            value = auth.strip()
            low = value.lower()
            if not (low.startswith("bearer ") or low.startswith("basic ")
                    or low.startswith("token ") or low.startswith("digest ")):
                # Se sembra un JWT, anteponi "Bearer "
                if _JWT_LIKE.match(value):
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {value}"
        return self.get_response(request)