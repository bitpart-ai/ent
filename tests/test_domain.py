from pathlib import Path

import pytest

from ent import util
from ent.lib.action import Action
from ent.lib.domain import Domain


@pytest.fixture
def transcript_rows() -> list[dict]:
    return util.get_rows(Path("tests/fixtures/transcript.csv"))


@pytest.fixture
def domain_from_rows(transcript_rows) -> Domain:
    return Domain.from_transcript_rows(transcript_rows)


def test_create_domain(domain_from_rows: Domain):
    assert domain_from_rows


def test_create_domain__tasks(domain_from_rows):
    task_names = [task.name for task in domain_from_rows.tasks.values()]
    assert len(set(task_names)) == 11


def test_create_domain__all_tasks_unique(domain_from_rows):
    task_names = [task.name for task in domain_from_rows.tasks.values()]
    assert len(set(task_names)) == len(task_names)


@pytest.mark.parametrize(
    "task_name,expected",
    [
        ("pass_time_at_baker_st", 3),
        ("read_novel", 1),
        ("smoke_pipe", 1),
        ("read_watsons_mind", 1),
        ("explain_deductive_method", 2),
        ("express_amazement", 2),
        ("explain_case", 1),
        ("decide_whether_to_help_holmes", 2),
        ("solve_case", 1),
        ("react_to_telegram", 2),
        ("leave", 3),
    ],
)
def test_create_domain__methods(task_name, expected, domain_from_rows):
    task = domain_from_rows.get_task_by_name(task_name)
    assert len(task.methods) == expected


@pytest.mark.parametrize(
    "task_name,observed_actions,expected",
    [
        (
            "read_novel",
            [
                Action("WATSON", "PICKS_UP", {"object": "novel"}),
                Action("WATSON", "SITS_DOWN", {"target": "armchair"}),
            ],
            ["It's far too hot out today to do anything but stay indoors."],
        ),
        (
            "smoke_pipe",
            [
                Action("HOLMES", "PICKS_UP", {"object": "tobacco"}),
                Action("HOLMES", "PLACES_IN", {"object": "tobacco", "target": "pipe"}),
                Action("HOLMES", "SMOKES", {"object": "pipe"}),
                Action(
                    "WATSON",
                    "SPEAKS_TO",
                    {
                        "target": "HOLMES",
                        "utterance": "Where ever did you get that slipper in which you keep your tobacco, Holmes?",
                    },
                ),
            ],
            ["That is too long a story for a day as hot as today, Doctor."],
        ),
        (
            "read_watsons_mind",
            [
                Action(
                    "HOLMES",
                    "SPEAKS_TO",
                    {
                        "target": "WATSON",
                        "utterance": "You are right, Watson, it does seem a most preposterous way of settling a dispute.",
                    },
                ),
                Action(
                    "WATSON",
                    "SPEAKS_TO",
                    {
                        "target": "HOLMES",
                        "utterance": "Most preposterous!",
                    },
                ),
                Action("WATSON", "STARES_AT", {"target": "HOLMES"}),
                Action("WATSON", "SPEAKS_TO", {"target": "HOLMES", "utterance": "What is this, Holmes?"}),
                Action(
                    "HOLMES",
                    "SPEAKS_TO",
                    {
                        "target": "WATSON",
                        "utterance": "When I saw you throw down your paper and enter upon a train of thought, I was very happy to have the opportunity of reading it off, and eventually of breaking into it, as a proof that I had been in rapport with you",
                    },
                ),
            ],
            [
                "A close reasoner follows the unspoken thoughts of his companion.",
                "I saw by the alteration in your face that a train of thought had been started.",
            ],
        ),
        (
            "read_watsons_mind",
            [
                Action(
                    "HOLMES",
                    "SPEAKS_TO",
                    {
                        "target": "WATSON",
                        "utterance": "You are right, Watson, it does seem a most preposterous way of settling a dispute.",
                    },
                ),
                Action(
                    "WATSON",
                    "SPEAKS_TO",
                    {
                        "target": "HOLMES",
                        "utterance": "Most preposterous!",
                    },
                ),
                Action("WATSON", "STARES_AT", {"target": "HOLMES"}),
                Action("WATSON", "SPEAKS_TO", {"target": "HOLMES", "utterance": "What is this, Holmes?"}),
                Action(
                    "HOLMES",
                    "SPEAKS_TO",
                    {
                        "target": "WATSON",
                        "utterance": "When I saw you throw down your paper and enter upon a train of thought, I was very happy to have the opportunity of reading it off, and eventually of breaking into it, as a proof that I had been in rapport with you",
                    },
                ),
                Action(
                    "HOLMES",
                    "SPEAKS_TO",
                    {
                        "target": "WATSON",
                        "utterance": "A close reasoner follows the unspoken thoughts of his companion.",
                    },
                ),
            ],
            [
                "You have followed me wonderfully!",
                "And now that you have explained it, I confess that I am as amazed as before.",
            ],
        ),
        (
            "solve_case",
            [
                Action(
                    "LESTRADE",
                    "SPEAKS_TO",
                    {"target": "HOLMES", "utterance": "A telegram for you, Mr. Holmes."},
                ),
                Action("LESTRADE", "GIVES", {"target": "HOLMES", "object": "telegram"}),
                Action("HOLMES", "SPEAKS_TO", {"target": "LESTRADE", "utterance": "Ha! It is the answer!"}),
                Action(
                    "LESTRADE",
                    "SPEAKS_TO",
                    {"target": "HOLMES", "utterance": "You are a miracle worker, Mr. Holmes!"},
                ),
            ],
            ["Good day!", "Until next time.", "Au revoir."],
        ),
    ],
)
def test_get_dialogue_choices(task_name, observed_actions, expected, domain_from_rows):
    choices = domain_from_rows.get_dialogue_choices(task_name, observed_actions)
    assert set(choice.details["utterance"] for choice in choices) == set(expected)
