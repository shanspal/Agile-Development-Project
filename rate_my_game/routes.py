from flask import render_template, request, redirect, url_for, jsonify, abort
from .database import db
from .models import Game, Rating, GameTag, PREDEFINED_TAGS


def register_routes(app):
    # ---------- HTML ROUTES ----------

    @app.route("/")
    def index():
        return render_template("index.html", tags=PREDEFINED_TAGS)

    @app.route("/games/<int:game_id>")
    def game_detail(game_id):
        game = Game.query.get_or_404(game_id)
        # Ensure all predefined tags exist for this game
        existing_tags = {t.tag_name: t for t in game.tags}
        for tag in PREDEFINED_TAGS:
            if tag not in existing_tags:
                gt = GameTag(game_id=game.id, tag_name=tag, count=0)
                db.session.add(gt)
        db.session.commit()
        game = Game.query.get(game_id)  # refresh with tags
        return render_template("game_detail.html", game=game, tags=PREDEFINED_TAGS)

    @app.route("/games/add", methods=["GET", "POST"])
    def add_game():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            company = request.form.get("company", "").strip()

            if not name or not company:
                return render_template(
                    "add_game.html",
                    error="Name and company are required.",
                )

            game = Game(name=name, company=company)
            db.session.add(game)
            db.session.commit()

            # Initialize tags for this game
            for tag in PREDEFINED_TAGS:
                gt = GameTag(game_id=game.id, tag_name=tag, count=0)
                db.session.add(gt)
            db.session.commit()

            return redirect(url_for("game_detail", game_id=game.id))

        return render_template("add_game.html")

    @app.route("/games/<int:game_id>/edit", methods=["GET", "POST"])
    def edit_game(game_id):
        game = Game.query.get_or_404(game_id)

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            company = request.form.get("company", "").strip()

            if not name or not company:
                return render_template(
                    "edit_game.html",
                    game=game,
                    error="Name and company are required.",
                )

            game.name = name
            game.company = company
            db.session.commit()
            return redirect(url_for("game_detail", game_id=game.id))

        return render_template("edit_game.html", game=game)

    @app.route("/games/<int:game_id>/delete", methods=["POST"])
    def delete_game(game_id):
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for("index"))

    # ---------- API ROUTES (JSON) ----------

    @app.route("/api/games")
    def api_get_games():
        search = request.args.get("search", "", type=str).strip()
        company = request.args.get("company", "", type=str).strip()
        tags = request.args.getlist("tags")
        sort = request.args.get("sort", "gameplay_desc", type=str)

        query = Game.query

        if search:
            like = f"%{search}%"
            query = query.filter(Game.name.ilike(like))

        if company:
            like = f"%{company}%"
            query = query.filter(Game.company.ilike(like))

        games = query.all()

        # Filter by tags (game must have all selected tags with count > 0)
        if tags:
            filtered = []
            for g in games:
                tag_map = {t.tag_name: t.count for t in g.tags}
                if all(tag_map.get(t, 0) > 0 for t in tags):
                    filtered.append(g)
            games = filtered

        # Sorting 

        if sort == "gameplay_desc":
            games.sort(
                key=lambda g: (g.average_gameplay() or 0),
                reverse=True
            )
        

        elif sort == "gameplay_asc":
            games.sort(
                key=lambda g: (g.average_gameplay() or 0)
            )

        elif sort == "difficulty_desc":
            games.sort(
                key=lambda g: (g.average_difficulty() or 0),
                reverse=True
            )

        elif sort == "difficulty_asc":
            games.sort(
                key=lambda g: (g.average_difficulty() or 0)
            )

        elif sort == "ratings_desc":
            games.sort(
                key=lambda g: len(g.ratings),
                reverse=True
            )

        elif sort == "alphabetical":
            games.sort(
                key=lambda g: g.name.lower()
            )
            

        result = []
        for g in games:
            result.append(
                {
                    "id": g.id,
                    "name": g.name,
                    "company": g.company,
                    "avg_gameplay": g.average_gameplay(),
                    "avg_difficulty": g.average_difficulty(),
                    "ratings_count": len(g.ratings),
                    "total_tag_votes": g.total_tag_votes(),
                }
            )

        return jsonify(result)

    @app.route("/api/games/<int:game_id>/ratings", methods=["POST"])
    def api_add_rating(game_id):
        game = Game.query.get_or_404(game_id)
        data = request.get_json() or {}
        gameplay = data.get("gameplay")
        difficulty = data.get("difficulty")

        try:
            gameplay = int(gameplay)
            difficulty = int(difficulty)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid rating values."}), 400

        if not (1 <= gameplay <= 5 and 1 <= difficulty <= 5):
            return jsonify({"error": "Ratings must be between 1 and 5."}), 400

        rating = Rating(game_id=game.id, gameplay=gameplay, difficulty=difficulty)
        db.session.add(rating)
        db.session.commit()

        return jsonify(
            {
                "message": "Rating added.",
                "avg_gameplay": game.average_gameplay(),
                "avg_difficulty": game.average_difficulty(),
                "ratings_count": len(game.ratings),
            }
        )

    @app.route("/api/games/<int:game_id>/tags/<tag_name>/vote", methods=["POST"])
    def api_vote_tag(game_id, tag_name):
        game = Game.query.get_or_404(game_id)
        if tag_name not in PREDEFINED_TAGS:
            return jsonify({"error": "Invalid tag."}), 400

        tag = GameTag.query.filter_by(game_id=game.id, tag_name=tag_name).first()
        if not tag:
            tag = GameTag(game_id=game.id, tag_name=tag_name, count=0)
            db.session.add(tag)

        tag.count += 1
        db.session.commit()

        return jsonify(
            {
                "message": "Tag vote recorded.",
                "tag_name": tag.tag_name,
                "count": tag.count,
            }
        )

    @app.route("/api/games/<int:game_id>/tags")
    def api_get_tags(game_id):
        game = Game.query.get_or_404(game_id)
        tags = [
            {"tag_name": t.tag_name, "count": t.count}
            for t in sorted(game.tags, key=lambda x: x.count, reverse=True)
        ]
        return jsonify(tags)
