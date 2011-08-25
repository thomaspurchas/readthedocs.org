import os
import glob
import shutil
from doc_builder.base import restoring_chdir
from doc_builder.backends.sphinx import Builder as HtmlBuilder
from projects.utils import run
from core.utils import copy_file_to_app_servers


from django.conf import settings


class Builder(HtmlBuilder):

    @restoring_chdir
    def build(self):
        project = self.version.project
        os.chdir(project.conf_dir(self.version.slug))
        if project.use_virtualenv and project.whitelisted:
            build_command = '%s -b pdf . _build/pdf' % project.venv_bin(
                version=self.version.slug, bin='sphinx-build')
        else:
            build_command = "sphinx-build -b pdf . _build/pdf"
        build_results = run(build_command)
        return build_results

    def move(self):
        project = self.version.project
        outputted_path = os.path.join(project.conf_dir(self.version.slug),
                                    '_build', 'pdf')
        to_path = os.path.join(settings.MEDIA_ROOT,
                               'pdf',
                               project.slug,
                               self.version.slug)
        from_file = os.path.join(outputted_path, "*.pdf")
        to_file = os.path.join(to_path, "%s.pdf" % project.slug)
        if getattr(settings, "MULTIPLE_APP_SERVERS", None):
            copy_file_to_app_servers(from_file, to_file)
        else:
            if not os.path.exists(to_path):
                os.makedirs(to_path)
            if os.path.exists(to_file):
                os.unlink(to_file)

            # Get a list of files that match the wildcard, and then only move
            # the first one. Seems to be more reliable than mv command.
            from_files = glob.glob(from_file)
            if len(from_files):
                shutil.move(from_files[0], to_file)
            else:
                print "Failed to move pdf file"
