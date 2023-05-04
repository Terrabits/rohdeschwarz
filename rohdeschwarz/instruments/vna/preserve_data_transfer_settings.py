

class PreserveDataTransferSettings:
    """provides a context manager for data transfer settings.

    On construction, `vna.settings` properties `data_format`
    and `byte_order` are saved. Settings are restored on
    context manager exit or destruction, whichever comes
    first.

    Arguments:
    vna -- Vna object
    """

    # life cycle

    def __init__(self, vna):
        """
        constructor
        saves data transfer settings for later restoration
        """
        self._settings = vna.settings
        self._save()


    def __del__(self):
        """destructor; restores data transfer settings"""
        self._restore()


    # context management

    def __enter__(self):
        """enter context manager"""
        pass


    def __exit__(self, *args):
        """exit context manager; restore data transfer settings"""
        self._restore()


    # helpers

    def _save(self):
        """save data transfer settings"""
        settings = self._settings
        self.data_format = settings.data_format
        self.byte_order  = settings.byte_order
        self.restore     = True


    def _restore(self):
        """restore data transfer settings"""

        # check restore
        if not self.restore:
            return

        # restore
        settings = self._settings
        settings.data_format = self.data_format
        settings.byte_order  = self.byte_order
        self.restore         = False
