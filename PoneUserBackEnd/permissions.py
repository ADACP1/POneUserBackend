from rest_framework import permissions
from rest_framework_simplejwt.tokens import UntypedToken

class IsMyAdmin(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo usuarios con rol 'admin'.
    """

    def has_permission(self, request, view):
        # Obtener el token JWT desde el encabezado Authorization
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            try:
                # Extraer el token después de 'Bearer '
                token = auth_header.split(' ')[0]
                # Decodificar el token
                untoken = UntypedToken(token)
                # Extraer los datos del payload
                payload = untoken.payload
                role = payload.get('role', None)
                # Verificar el rol
                return role == 'user'
            except Exception as e:
                print(f"Error extracting token or payload: {e}")
                return False
        return False