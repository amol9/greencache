
from redlib.api.system import is_windows


home_dir_name = 'greencache' if is_windows() else '.greencache
most_recent_dt_cache_filename = 'mr_datetime'
