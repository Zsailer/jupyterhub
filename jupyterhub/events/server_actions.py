import sys
from enum import Enum
from pydantic import BaseModel, Schema
from textwrap import dedent

from jupyter_telemetry import Event


if sys.version_info[:2] < (3, 6):
    raise ValueError("Jupyter's Events API does not support Python < 3.6: %s" % sys.version)

VERSION = 1

class Actions(str, Enum):
    start = 'start'
    stop = 'stop'
    

class JupyterHubServerEvents(Event):
    """Record actions on user servers made via JupyterHub.

    JupyterHub can perform various actions on user servers via 
    direct interaction from users, or via the API. This event is 
    recorded whenever either of those happen.

    Limitations:

    1. This does not record all server starts / stops, only those
       explicitly performed by JupyterHub. For example, a user's server
       can go down because the node it was running on dies. That will
       not cause an event to be recorded, since it was not initiated
       by JupyterHub. In practice this happens often, so this is not
       a complete record.

    2. Events are only recorded when an action succeeds.
    """
    _id = "hub.jupyter.org/server-action"
    _title = "JupyterHub server events"
    _version = VERSION

    action: Actions = Schema(..., 
        title='action',
        description=dedent("""\
        Action performed by JupyterHub.

        This is a required field.

        Possible Values:

        - start: a user's server was successfully started
        - stop: a user's server was successfully stopped
        """),
    )

    username: str = Schema(...,
        title='username',
        description=dedent("""\
        Name of the user whose server this action was performed on.

        This is the normalized name used by JupyterHub itself,
        which is derived from the authentication provider used but 
        might not be the same as used in the authentication provider.
        """)
    )
    
    servername: str = Schema(...,
        title='servername',
        description=dedent("""\
        Name of the server this action was performed on.

        JupyterHub supports each user having multiple servers with
        arbitrary names, and this field specifies the name of the
        server.

        The 'default' server is denoted by the empty string
        """)
    )
