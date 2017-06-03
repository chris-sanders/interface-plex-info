from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log

class PlexInfoRequires(RelationBase):
    scope = scopes.GLOBAL
    auto_accessors=['hostname','port','user','passwd']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state('{relation_name}.triggered'))

    @hook('{requires:plex-info}-relation-{joined,changed}')
    def changed(self):
        log('plex-info.available','INFO')
        self.set_state('{relation_name}.available')
        if self.hostname() and self.port() and self.user() and self.passwd():
            log('plex-info.triggered','INFO')
            self.set_state('{relation_name}.triggered')
            if self.hostname() != self.get_local('hostname') or\
               self.port() != self.get_local('port') or \
               self.user() != self.get_local('user') or \
               self.passwd() != self.get_local('passwd'):
                self.set_local('hostname',self.hostname())
                self.set_local('port',self.port())
                self.set_local('user',self.user())
                self.set_local('passwd',self.passwd())
                self.remove_state('{relation_name}.configured')

    @hook('{requires:plex-info}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.configured')
        log('Removed plex-info.configured','INFO')

    def configured(self):
        self.set_state('{relation_name}.configured')
