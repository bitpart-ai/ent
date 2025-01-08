import dataclasses
from typing import Optional
from uuid import UUID, uuid4

from ent.lib.action import Action
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

    def get_dialogue_choices(self, task_name: str, observed_actions: list[Action]) -> list[Action]:
        # TODO: for a given root-level task and a sequence of already-observed Actions,
        # determine what SPEAKS_TO actions could follow as the next action.
        raise NotImplementedError
