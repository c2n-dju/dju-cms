class DataRouter(object):
    """
    A router to control all database operations on models in the
    intra applications.
    """
    def db_for_read(self, model, **hints):
        #print("? " + str(model._meta.app_label))
        #print("?? " + str(model._meta))
        if model._meta.app_label[-5:] == "_core":
            #print("-> dbcore")
            return "dbcore"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label[-5:] == "_core":
            return "dbcore"
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        different-data scenario, we reject any relations between two different databases
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the *.core app only appears in the "dbcore" database
        """
        if app_label[-5:] == "_core":
            return db == "dbcore"
        return None
