import dataclasses
from uuid import UUID

from ent.lib.task import Task


@dataclasses.dataclass
class Domain:
    """A domain is a container that holds tasks. Taken as a whole, it is a set of behaviors
    or narrative episodes for a set of characters along with objects they can interact with.
    """

    uuid: UUID
    name: str
    tasks: dict[UUID, Task]

    @classmethod
    def from_transcript_rows(cls, rows: list[dict]) -> "Domain":
        # TODO: create a domain given rows of a transcript
        raise NotImplementedError
