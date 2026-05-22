from rate_my_game import create_app
from rate_my_game.database import db
from rate_my_game.models import Game, GameTag

app = create_app()

games = [
    ("Baldur's Gate 3", "Larian Studios", "RPG|Singleplayer|Story-Rich|Strategy"),
    ("Elden Ring", "FromSoftware", "Action|RPG|Singleplayer|Open World"),
    ("The Legend of Zelda: Breath of the Wild", "Nintendo", "Action|RPG|Singleplayer|Open World"),
    ("The Legend of Zelda: Ocarina of Time", "Nintendo", "Action|RPG|Singleplayer|Story-Rich"),
    ("Red Dead Redemption 2", "Rockstar Games", "Action|Singleplayer|Story-Rich|Open World"),
    ("The Witcher 3: Wild Hunt", "CD Projekt Red", "RPG|Singleplayer|Story-Rich|Open World"),
    ("Portal 2", "Valve", "Puzzle|Singleplayer|Story-Rich"),
    ("Half-Life 2", "Valve", "Action|Singleplayer|Story-Rich"),
    ("Super Mario Odyssey", "Nintendo", "Action|Singleplayer|Casual"),
    ("God of War", "Santa Monica Studio", "Action|Singleplayer|Story-Rich"),
    ("The Last of Us", "Naughty Dog", "Action|Singleplayer|Story-Rich|Horror"),
    ("Hades", "Supergiant Games", "Action|RPG|Singleplayer|Indie"),
    ("Mass Effect 2", "BioWare", "RPG|Singleplayer|Story-Rich"),
    ("Persona 5 Royal", "Atlus", "RPG|Singleplayer|Story-Rich"),
    ("Disco Elysium", "ZA/UM", "RPG|Singleplayer|Story-Rich|Indie"),
    ("Hollow Knight", "Team Cherry", "Action|Singleplayer|Indie"),
    ("Stardew Valley", "ConcernedApe", "Casual|Singleplayer|Indie"),
    ("Terraria", "Re-Logic", "Action|RPG|Multiplayer|Indie"),
    ("Resident Evil 4", "Capcom", "Action|Singleplayer|Horror"),
    ("Dark Souls III", "FromSoftware", "Action|RPG|Singleplayer"),
    ("Sekiro: Shadows Die Twice", "FromSoftware", "Action|Singleplayer"),
    ("Super Mario Galaxy", "Nintendo", "Action|Singleplayer|Casual"),
    ("Grand Theft Auto V", "Rockstar Games", "Action|Multiplayer|Open World"),
    ("Metal Gear Solid 3: Snake Eater", "Konami", "Action|Singleplayer|Story-Rich"),
    ("BioShock", "2K Games", "Action|Singleplayer|Story-Rich|Horror"),
    ("Minecraft", "Mojang Studios", "Casual|Multiplayer|Open World"),
    ("Slay the Spire", "Mega Crit", "Strategy|Singleplayer|Indie"),
    ("Celeste", "Maddy Makes Games", "Action|Singleplayer|Indie"),
    ("Divinity: Original Sin 2", "Larian Studios", "RPG|Multiplayer|Story-Rich|Strategy"),
    ("NieR: Automata", "PlatinumGames", "Action|RPG|Singleplayer|Story-Rich"),
    ("The Elder Scrolls V: Skyrim", "Bethesda Game Studios", "RPG|Singleplayer|Open World"),
    ("Chrono Trigger", "Square Enix", "RPG|Singleplayer|Story-Rich"),
    ("Final Fantasy VII Remake", "Square Enix", "Action|RPG|Singleplayer|Story-Rich"),
    ("Final Fantasy X", "Square Enix", "RPG|Singleplayer|Story-Rich"),
    ("Dragon Age: Origins", "BioWare", "RPG|Singleplayer|Story-Rich|Strategy"),
    ("Fallout: New Vegas", "Obsidian Entertainment", "RPG|Singleplayer|Story-Rich|Open World"),
    ("Cyberpunk 2077", "CD Projekt Red", "Action|RPG|Singleplayer|Open World"),
    ("Monster Hunter: World", "Capcom", "Action|RPG|Multiplayer"),
    ("Devil May Cry 5", "Capcom", "Action|Singleplayer"),
    ("Bayonetta", "PlatinumGames", "Action|Singleplayer"),
    ("DOOM Eternal", "id Software", "Action|Singleplayer"),
    ("Halo 3", "Bungie", "Action|Multiplayer|Competitive"),
    ("Apex Legends", "Respawn Entertainment", "Action|Multiplayer|Competitive"),
    ("Counter-Strike 2", "Valve", "Action|Multiplayer|Competitive"),
    ("Valorant", "Riot Games", "Action|Multiplayer|Competitive"),
    ("League of Legends", "Riot Games", "Multiplayer|Competitive|Strategy"),
    ("Dota 2", "Valve", "Multiplayer|Competitive|Strategy"),
    ("Overwatch 2", "Blizzard Entertainment", "Action|Multiplayer|Competitive"),
    ("Fortnite", "Epic Games", "Action|Multiplayer|Competitive"),
    ("Rocket League", "Psyonix", "Multiplayer|Competitive|Casual"),
    ("Tom Clancy's Rainbow Six Siege", "Ubisoft", "Action|Multiplayer|Competitive|Strategy"),
    ("Street Fighter 6", "Capcom", "Action|Multiplayer|Competitive"),
    ("Tekken 8", "Bandai Namco Studios", "Action|Multiplayer|Competitive"),
    ("Sid Meier's Civilization VI", "Firaxis Games", "Strategy|Singleplayer|Multiplayer"),
    ("XCOM 2", "Firaxis Games", "Strategy|Singleplayer"),
    ("StarCraft II", "Blizzard Entertainment", "Strategy|Multiplayer|Competitive"),
    ("Age of Empires II: Definitive Edition", "Forgotten Empires", "Strategy|Multiplayer|Competitive"),
    ("Total War: Warhammer III", "Creative Assembly", "Strategy|Singleplayer|Multiplayer"),
    ("Crusader Kings III", "Paradox Development Studio", "Strategy|Singleplayer"),
    ("RimWorld", "Ludeon Studios", "Strategy|Singleplayer|Indie"),
    ("Factorio", "Wube Software", "Strategy|Singleplayer|Multiplayer|Indie"),
    ("Cities: Skylines", "Colossal Order", "Strategy|Singleplayer|Casual"),
    ("The Sims 4", "Maxis", "Casual|Singleplayer"),
    ("Animal Crossing: New Horizons", "Nintendo", "Casual|Singleplayer|Multiplayer"),
    ("Dave the Diver", "MINTROCKET", "Casual|RPG|Singleplayer|Indie"),
    ("Balatro", "LocalThunk", "Strategy|Singleplayer|Indie|Casual"),
    ("Vampire Survivors", "poncle", "Action|Casual|Singleplayer|Indie"),
    ("Undertale", "Toby Fox", "RPG|Singleplayer|Story-Rich|Indie"),
    ("Cuphead", "Studio MDHR", "Action|Singleplayer|Indie"),
    ("Dead Cells", "Motion Twin", "Action|Singleplayer|Indie"),
    ("Ori and the Will of the Wisps", "Moon Studios", "Action|Singleplayer|Story-Rich"),
    ("INSIDE", "Playdead", "Puzzle|Singleplayer|Story-Rich|Indie"),
    ("Limbo", "Playdead", "Puzzle|Singleplayer|Horror|Indie"),
    ("Return of the Obra Dinn", "Lucas Pope", "Puzzle|Singleplayer|Indie"),
    ("The Witness", "Thekla", "Puzzle|Singleplayer|Indie"),
    ("Baba Is You", "Hempuli", "Puzzle|Singleplayer|Indie"),
    ("Tetris Effect: Connected", "Enhance", "Puzzle|Casual|Multiplayer"),
    ("It Takes Two", "Hazelight Studios", "Action|Puzzle|Multiplayer|Story-Rich"),
    ("Among Us", "Innersloth", "Casual|Multiplayer|Indie"),
    ("Phasmophobia", "Kinetic Games", "Horror|Multiplayer|Indie"),
    ("Resident Evil 2", "Capcom", "Action|Singleplayer|Horror"),
    ("Silent Hill 2", "Konami", "Singleplayer|Story-Rich|Horror"),
    ("Dead Space", "EA Redwood Shores", "Action|Singleplayer|Horror"),
    ("Alien: Isolation", "Creative Assembly", "Singleplayer|Horror"),
    ("Amnesia: The Dark Descent", "Frictional Games", "Singleplayer|Horror|Indie"),
    ("Outlast", "Red Barrels", "Singleplayer|Horror|Indie"),
    ("Subnautica", "Unknown Worlds Entertainment", "Singleplayer|Open World|Horror|Indie"),
    ("No Man's Sky", "Hello Games", "Singleplayer|Multiplayer|Open World|Indie"),
    ("Forza Horizon 5", "Playground Games", "Casual|Multiplayer|Open World"),
    ("Microsoft Flight Simulator", "Asobo Studio", "Singleplayer|Casual"),
    ("Firewatch", "Campo Santo", "Singleplayer|Story-Rich|Indie"),
    ("Life is Strange", "Dontnod Entertainment", "Singleplayer|Story-Rich"),
    ("Detroit: Become Human", "Quantic Dream", "Singleplayer|Story-Rich"),
    ("What Remains of Edith Finch", "Giant Sparrow", "Singleplayer|Story-Rich|Indie"),
    ("A Plague Tale: Innocence", "Asobo Studio", "Action|Singleplayer|Story-Rich"),
    ("Tomb Raider", "Crystal Dynamics", "Action|Singleplayer|Story-Rich"),
    ("Assassin's Creed Odyssey", "Ubisoft Quebec", "Action|RPG|Singleplayer|Open World"),
    ("Ghost of Tsushima", "Sucker Punch Productions", "Action|Singleplayer|Story-Rich|Open World"),
    ("Horizon Zero Dawn", "Guerrilla Games", "Action|RPG|Singleplayer|Open World"),
    ("Outer Wilds", "Mobius Digital", "Puzzle|Singleplayer|Story-Rich|Indie"),
]

with app.app_context():
    db.create_all()

    for name, company, tags in games:
        if Game.query.filter_by(name=name, company=company).first():
            continue

        game = Game(name=name, company=company)
        db.session.add(game)
        db.session.flush()

        for tag_name in tags.split("|"):
            db.session.add(GameTag(game_id=game.id, tag_name=tag_name.strip()))
    db.session.commit()
    print("Seeded games:", len(games))