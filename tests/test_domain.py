from pathlib import Path

import pytest

from ent import util
from ent.lib.domain import Domain


@pytest.fixture
def transcript_rows() -> list[dict]:
    return util.get_rows(Path("tests/fixtures/transcript.csv"))


@pytest.fixture
def domain_from_rows(transcript_rows) -> Domain:
    return Domain.from_transcript_rows(transcript_rows)


def test_create_domain(domain_from_rows: Domain):
    assert domain_from_rows


def test_create_domain__root_tasks(domain_from_rows):
    task_names = [task.name for task in domain_from_rows.tasks.values()]
    assert len(set(task_names)) == 10


def test_create_domain__all_root_tasks_unique(domain_from_rows):
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
    ],
)
def test_create_domain__methods(task_name, expected, domain_from_rows):
    task = domain_from_rows.get_task_by_name(task_name)
    assert len(task.methods) == expected
