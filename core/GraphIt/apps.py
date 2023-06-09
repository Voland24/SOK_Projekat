from django.apps import AppConfig
import pkg_resources

class GraphitConfig(AppConfig):
    name = 'GraphIt'
    load_components = []
    display_components = []

    def ready(self):
        self.load_components = load_components('data.load')
        self.display_components = load_components('data.display')

def load_components(name: str) -> list:
    #Loads all components by finding them using component name
    components = []
    for ep in pkg_resources.iter_entry_points(group = name):
        c = ep.load()
        component = c()
        components.append(component)
    return components