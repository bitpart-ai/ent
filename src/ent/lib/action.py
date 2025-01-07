import dataclasses
from uuid import UUID, uuid4


@dataclasses.dataclass(frozen=True)
class Action:
    """An action is a concrete step taken by an actor (called `character` here).

    `details` are the bindings for an instance of an action, e.g., for a 'PICKS_UP'
    action, we must bind the variable 'object' to the object to be picked up. For our current
    purposes, these bindings are supplied by the transcript data.
    """

    character: str
    verb: str
    details: dict[str, str]
    uuid: UUID = dataclasses.field(default_factory=uuid4)
