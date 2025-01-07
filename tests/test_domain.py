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


def test_create_domain_from_transcript_rows(domain_from_rows):
    assert domain_from_rows


def test_create_domain_root_tasks(domain_from_rows):
    pass


def test_create_domain_subtasks(domain_from_rows):
    pass
