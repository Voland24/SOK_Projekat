from GraphIt.services.services import GraphViewService
import os
from sys import platform


class ClassViewLoader(GraphViewService):
    def identification(self):
        return 'class_view_loader'

    def name(self):
        return 'class_view_loader'

    def get_script_path(self) -> str:
        """Function that returns javascript file path"""
        start = 'tim11'
        path = 'class_view/class_view/scripts/class_view.js'
        rel = os.path.relpath(path, start).replace("\\", "/")

        if platform == "darwin":
            return path

        return rel