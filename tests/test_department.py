import pytest


@pytest.mark.asyncio
async def test_create_department(client):
    response = await client.post(
        "/departments/",
        json={
            "name": "Test Department",
            "parent_id": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Department"
    assert data["parent_id"] is None

@pytest.mark.asyncio
async def test_unique_department_name(client):
    await client.post(
        "/departments/",
        json={"name": "Unique Dept", "parent_id": None},
    )

    response = await client.post(
        "/departments/",
        json={"name": "Unique Dept", "parent_id": None},
    )

    assert response.status_code == 400

@pytest.mark.asyncio
async def test_department_tree(client):
    root = await client.post(
        "/departments/",
        json={"name": "Root Dept", "parent_id": None},
    )
    root_id = root.json()["id"]

    child = await client.post(
        "/departments/",
        json={"name": "Child Dept", "parent_id": root_id},
    )

    tree = await client.get(f"/departments/{root_id}/tree")

    assert tree.status_code == 200
    data = tree.json()
    assert len(data["children"]) == 1