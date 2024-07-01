from pymoo.util.archive import Archive

# Stores all individuals added to the archive
# Duplicate elemination is applied using default strategy

class MemoryArchive(Archive):
    def __new__(cls, **kwargs):
        return super().__new__(cls,
                                **kwargs)

    def _find_opt(self, sols):
        # do nothing
        return sols