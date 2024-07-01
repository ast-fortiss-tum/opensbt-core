from pymoo.util.archive import Archive

# Stores all individuals added to the archive

class MemoryArchive(Archive):
    def __new__(cls,
                **kwargs):
        kwargs["duplicate_elimination"] = None
        return super().__new__(cls,
                                **kwargs)

    def _find_opt(self, sols):
        # do nothing
        return sols