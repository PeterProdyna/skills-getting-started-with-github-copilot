def test_get_activities_returns_all_activities(client, fresh_activities):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_activity in data


def test_signup_adds_student_to_activity(client, fresh_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in fresh_activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client, fresh_activities):
    # Arrange
    activity_name = "Unknown Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_returns_400(client, fresh_activities):
    # Arrange
    activity_name = "Chess Club"
    email = fresh_activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_student_from_activity(client, fresh_activities):
    # Arrange
    activity_name = "Chess Club"
    email = fresh_activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in fresh_activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client, fresh_activities):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_member_returns_404(client, fresh_activities):
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_signup_then_unregister_lifecycle(client, fresh_activities):
    # Arrange
    activity_name = "Science Club"
    email = "lifecycle@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    list_after_signup = client.get("/activities")
    unregister_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    list_after_unregister = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert email in list_after_signup.json()[activity_name]["participants"]
    assert unregister_response.status_code == 200
    assert email not in list_after_unregister.json()[activity_name]["participants"]