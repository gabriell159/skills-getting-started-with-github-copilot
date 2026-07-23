import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(scope="function")
def client():
    original_activities = copy.deepcopy(activities)
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))
