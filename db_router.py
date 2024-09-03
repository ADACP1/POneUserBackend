class AdminDatabaseRouter:
    def db_for_read(self, model, **hints):
        # Redirigir las lecturas de 'core' y 'tenants' a 'admindatabase'
        if model._meta.app_label in ['core']:
            return 'admindatabase'
        return None
"""
    def db_for_write(self, model, **hints):
        # Redirigir las escrituras de 'core' y 'tenants' a 'admindatabase'
        if model._meta.app_label in ['core', 'tenants']:
            return 'admindatabase'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Permitir relaciones si ambas instancias pertenecen a 'default' o 'admindatabase'
        if obj1._state.db in ('default', 'admindatabase') and obj2._state.db in ('default', 'admindatabase'):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # No permitir migraciones para 'core' y 'tenants'
        if app_label in ['core', 'tenants']:
            return False
        return None



    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permitir migraciones solo en 'admindatabase' para 'core' y 'tenants'
        if app_label in ['core', 'tenants']:
            return db == 'admindatabase'
        return None
"""