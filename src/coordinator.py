from pathlib import Path


class Coordinator:
    """Provides paths to main folders.

    Initializes paths to `root`, `src`, etc.
    Every field is a member of Path, not str.

        Usage example::
            # From a notebook
            c = Coordinator()
            c.root
            > '/opt/shared/user'
            c.data_interim
            > '/opt/shared/user/data/interim'
    """

    def __init__(self, path=None):

        if not path:
            self.root = Path(__file__).parents[1]
        else:
            self.root = Path(path).resolve()

        self.configs = self.root.joinpath('configs')
        self.notebooks = self.root.joinpath('notebooks')
        self.models = self.root.joinpath('models')
        self.reports = self.root.joinpath('reports')
        self.dotenv = self.root.joinpath('.env')
        self.data = self.root.joinpath('data')

        self.data_raw = self.data.joinpath('raw')
        self.data_interim = self.data.joinpath('interim')
        self.data_external = self.data.joinpath('external')
        self.data_processed = self.data.joinpath('processed')
