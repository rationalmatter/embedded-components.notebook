#
# Copyright (C) 2021, Rational Matter Ltd. All rights Reserved
#
# This software and/or source code may be used, copied and/or disseminated only with the written
# permission of Rational Matter Ltd, or in accordance with the terms and conditions stipulated in the
# agreement/contract under which the software and/or source code has been supplied by Rational Matter Ltd or
# its affiliates. Unauthorized use, copying, or dissemination of this file, via any medium, is strictly
# prohibited, and will constitute an infringement of copyright.
#

from notebook.services.contents.largefilemanager import LargeFileManager
from tornado import web
from io import StringIO
import nbformat
import junoapp

class JunoFileManager(LargeFileManager):
    def rename_file(self, old_path, new_path):
        """Rename a file."""
        print('[JunoFileManager] Renaming a file on disk')
        new_os_path = self._get_os_path(new_path.strip('/'))
        old_os_path = self._get_os_path(old_path.strip('/'))

        # Move the file
        try:
            junoapp.rename_notebook(old_os_path, new_os_path)
        except:
            raise web.HTTPError(500, u'Error renaming file: %s' % (old_path))

    def _save_notebook(self, os_path, nb):
        """Save a notebook to an os_path."""
        print('[JunoFileManager] Saving notebook to disk')
        data_container = StringIO()
        nbformat.write(nb, data_container, version=nbformat.NO_CONVERT)
        junoapp.write_notebook_data(os_path, data_container.getvalue())

    def _read_notebook(self, os_path, as_version=4):
        """Read a notebook from an os path."""
        print('[JunoFileManager] Reading notebook from disk')
        try:
            notebook_content = junoapp.read_notebook_data(os_path)
            return nbformat.read(StringIO(notebook_content), as_version=as_version)
        except Exception as e:
            print('[JunoFileManager] Error reading notebook from disk')
            print(e)
            raise web.HTTPError(400, u"Unreadable Notebook: %s" % (os_path))

    def check_and_sign(self, nb, path):
        try:
            super().check_and_sign(nb, path)
        except Exception as e:
            print(f'[JunoFileManager] Failed to sign the notebook while saving: {e}')
