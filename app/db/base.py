# import these here for Alembic
from app.db.base_class import Base  # noqa
from app.models.cast import Actor  # noqa
from app.models.cast import ActorDrama  # noqa
from app.models.cast import Cinematographer  # noqa
from app.models.cast import CinematographerDrama  # noqa
from app.models.cast import Composer  # noqa
from app.models.cast import ComposerDrama  # noqa
from app.models.cast import Director  # noqa
from app.models.cast import DirectorDrama  # noqa
from app.models.cast import Screenwriter  # noqa
from app.models.cast import ScreenwriterDrama  # noqa
from app.models.drama import Drama  # noqa
from app.models.drama import DramaGenre  # noqa
from app.models.drama import DramaTag  # noqa
from app.models.drama import Genre  # noqa
from app.models.drama import IDCache  # noqa
from app.models.drama import Tag  # noqa
from app.models.user import User  # noqa
from app.models.watchlist import Completed  # noqa
from app.models.watchlist import CurrentlyWatching  # noqa
from app.models.watchlist import Dropped  # noqa
from app.models.watchlist import OnHold  # noqa
from app.models.watchlist import PlanToWatch  # noqa
from app.models.watchlist import Watchlist  # noqa
