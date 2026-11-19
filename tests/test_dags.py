from pathlib import Path

import pytest
from airflow.dag_processing.dagbag import DagBag


@pytest.fixture(scope="module")
def dagbag():
    project_folder = Path(__file__).resolve().parents[1]

    return DagBag(
        dag_folder=str(project_folder / "dags"),
    )


def test_no_import_errors(dagbag):
    assert not dagbag.import_errors, dagbag.import_errors


def test_example_dag_exists(dagbag):
    assert "example_dag" in dagbag.dags


def test_task_structure(dagbag):
    dag = dagbag.dags["example_dag"]

    assert set(dag.task_ids) == {"extract", "transform", "load"}
    assert dag.get_task("extract").downstream_task_ids == {"transform"}
    assert dag.get_task("transform").downstream_task_ids == {"load"}
    assert dag.get_task("load").downstream_task_ids == set()
