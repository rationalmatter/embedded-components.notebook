#
# Copyright (C) 2021, Rational Matter Ltd. All rights Reserved
#
# This software and/or source code may be used, copied and/or disseminated only with the written
# permission of Rational Matter Ltd, or in accordance with the terms and conditions stipulated in the
# agreement/contract under which the software and/or source code has been supplied by Rational Matter Ltd or
# its affiliates. Unauthorized use, copying, or dissemination of this file, via any medium, is strictly
# prohibited, and will constitute an infringement of copyright.
#

from notebook.services.contents.filecheckpoints import FileCheckpoints

class JunoFileCheckpoints(FileCheckpoints):

    def checkpoint_path(self, checkpoint_id, path):
        print('[JunoFileCheckpoints] [Disabled] checkpoint_path(...)')
        return None

    def checkpoint_model(self, checkpoint_id, os_path):
        print('[JunoFileCheckpoints] [Disabled] checkpoint_model(...)')
        return dict()

    def create_checkpoint(self, contents_mgr, path):
        print('[JunoFileCheckpoints] [Disabled] create_checkpoint(...)')
        return dict()

    def restore_checkpoint(self, contents_mgr, checkpoint_id, path):
        print('[JunoFileCheckpoints] [Disabled] restore_checkpoint(...)')
        pass

    def rename_checkpoint(self, checkpoint_id, old_path, new_path):
        print('[JunoFileCheckpoints] [Disabled] rename_checkpoint(...)')
        pass

    def delete_checkpoint(self, checkpoint_id, path):
        print('[JunoFileCheckpoints] [Disabled] delete_checkpoint(...)')
        pass

    def list_checkpoints(self, path):
        print('[JunoFileCheckpoints] [Disabled] list_checkpoints(...)')
        return [dict()]
