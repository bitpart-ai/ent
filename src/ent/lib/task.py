import dataclasses
from uuid import UUID, uuid4

from ent.lib.action import Action


@dataclasses.dataclass
class Task:
    """A task corresponds very roughly to a goal or a unit of behavior or narrative.

    The canonical example from HTN planning is a task 'travel from home to park'. Concretely,
    a `Task` here is a collection of `TaskMethod`s that satisfy a task. An HTN planner would
    be given a task to accomplish, and would attempt to do so by selecting from among that task's
    methods.
    """

    name: str
    methods: list["TaskMethod"]
    uuid: UUID = dataclasses.field(default_factory=uuid4)


@dataclasses.dataclass
class TaskMethod:
    """A task method is a sequence of steps that satisfies a task. The steps of a task method can
    themselves be tasks (further expanding into their constituent steps) or actions (primitive concrete
    steps).

    For the canonical example task 'travel from home to park', we may have task methods such as

        [call taxi to home, ride taxi to park, pay driver]
        [get bike from garage, ride bike to park]
        [get car from garage, drive car to park]
        [walk to park]

    Each method is a different way to satisfy the parent task.
    """

    task_uuid: UUID
    children: list[Task | Action]
    uuid: UUID = dataclasses.field(default_factory=uuid4)
