import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture
def fresh_activities(monkeypatch):
    activities_copy = copy.deepcopy(INITIAL_ACTIVITIES)
    monkeypatch.setattr(app_module, "activities", activities_copy)
    return activities_copy