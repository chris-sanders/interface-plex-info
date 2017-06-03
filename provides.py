from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import log

class PlexInfoProvides(RelationBase):
    scope = scopes.GLOBAL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state('{relation_name}.triggered'))

    @hook('{provides:plex-info}-relation-{joined,changed}')
    def changed(self):
        log('plex-info.triggered','INFO')
        self.set_state('{relation_name}.available')
        self.set_state('{relation_name}.triggered')

    @hook('{provides:plex-info}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.configured')
        log('Removed plex-info.configured','INFO')

    def configure(self,hostname,port,user,passwd):
        relation_info = {
            'hostname': hostname,
            'port': port,
            'user': user,
            'passwd': passwd
             }
        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')
        log('plex-info.configured','INFO')
