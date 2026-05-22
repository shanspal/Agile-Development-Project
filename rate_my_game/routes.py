from functools import wraps

from flask import render_template, request, redirect, url_for, jsonify, abort, session
from werkzeug.security import check_password_hash, generate_password_hash
from .database import db
from .models import Game, Rating, GameTag, PREDEFINED_TAGS, User

def register_routes(app):
    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                return redirect(url_for("login", next=request.path))
            return view(*args, **kwargs)

        return wrapped

    # ---------- HTML ROUTES ----------

    @app.route("/")
    def index():
        return render_template("index.html", tags=PREDEFINED_TAGS)

    @app.route("/ranks")
    def ranks():
        games = Game.query.all()
        games.sort(key=lambda g: (g.average_gameplay() or 0), reverse=True)
        return render_template("ranks.html", games=games)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            if not username or not email or not password:
                return render_template(
                    "register.html",
                    error="Username, email, and password are required.",
                )

            if User.query.filter_by(username=username).first():
                return render_template("register.html", error="Username is already taken.")

            if User.query.filter_by(email=email).first():
                return render_template("register.html", error="Email is already registered.")

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        next_url = request.args.get("next") or url_for("index")

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                return render_template("login.html", error="Username and password are required.", next=next_url)

            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password_hash, password):
                return render_template("login.html", error="Invalid username or password.", next=next_url)

            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(next_url)

        return render_template("login.html", next=next_url)

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("index"))

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
    @login_required
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
        sort = request.args.get("sort", "avg_gameplay", type=str)

        query = Game.query

        if search:
            like = f"%{search}%"
            query = query.filter(Game.name.ilike(like))

        if company:
            like = f"%{company}%"
            query = query.filter(Game.company.ilike(like))

        games = query.all()

        if tags:
            filtered = []
            for g in games:
                tag_map = {t.tag_name: t.count for t in g.tags}
                if all(tag_map.get(t, 0) > 0 for t in tags):
                    filtered.append(g)
            games = filtered

        if sort == "name":
            games.sort(key=lambda g: g.name.lower())
        elif sort == "avg_gameplay":
            games.sort(key=lambda g: (g.average_gameplay() or 0), reverse=True)
        elif sort == "avg_difficulty":
            games.sort(key=lambda g: (g.average_difficulty() or 0), reverse=True)
        else:
            games.sort(key=lambda g: (g.average_gameplay() or 0), reverse=True)

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
