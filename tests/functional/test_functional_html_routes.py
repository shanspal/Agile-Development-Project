#Feature 1:Homepage can load successfully
def test_home_page_can_load(client):
    response = client.get('/')
    assert response.status_code == 200

#Feature 2:Add Game page cna load successfully
def test_add_game_page_can_load(client):
    response = client.get('/games/add')
    assert response.status_code == 200

#Feature 3:Add Game form can create a new game
def test_add_game_from_can_create(client):
    response = client.post(
        '/games/add',
        data={
            "name":"Test Game",
            "company":"Test Company",
        },
    )
    assert response.status_code == 302

#Feature 4:Game detail page can load successfully
def test_game_detail_page_can_load(client,sample_game):
    response = client.get(f"/games/{sample_game}")
    assert response.status_code == 200

