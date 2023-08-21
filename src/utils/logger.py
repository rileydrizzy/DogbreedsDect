"""doc

"""

from pathlib import Path
import mlflow
from loguru import logger

FORMAT_STYLE = (
    "{time:MMMM D, YYYY > HH:mm:ss}  | {level} | {module}: {function}{line} - {message}"
)

LOG_DIR = Path("logs")
log_filepath = Path(LOG_DIR, "running_logs.log")
Path.mkdir(LOG_DIR, exist_ok=True)

logger.add(
    log_filepath,
    format=FORMAT_STYLE,
    level="INFO",
)

def tracking(name):
    """_summary_

    Parameters
    ----------
    name : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    mlflow.set_tracking_uri('https://dagshub.com/rileydrizzy/dogbreeds_dect.mlflow')
    experiment = mlflow.get_experiment_by_name(name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(name)
        return experiment_id
    return experiment.experiment_id
