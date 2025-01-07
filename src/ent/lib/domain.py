import dataclasses
from typing import Optional
from uuid import UUID, uuid4

from ent.lib.task import Task


@dataclasses.dataclass
class Domain:
    """A domain is a container that holds tasks. Taken as a whole, it is a set of behaviors
    or narrative episodes for a set of characters along with objects they can interact with.
    """

    name: str
    tasks: dict[UUID, Task]
    uuid: UUID = dataclasses.field(default_factory=uuid4)

    @classmethod
    def from_transcript_rows(cls, rows: list[dict], name: str = "unnamed") -> "Domain":
        # TODO: create a domain from rows of a transcript
        raise NotImplementedError

    def get_task_by_name(self, name: str) -> Optional[Task]:
        for task in self.tasks.values():
            if task.name == name:
                return task
        return None
