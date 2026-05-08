# This is a README.md file

## ACIT 2911 - Agile Development Project

# 1. Overview

My project is a small full-stack web app called **Rate My Game**.

It lets users add games, rate them, tag them, comment on them, search them, and compare them.

It works like a mini version of RateMyProf, but for video games.

---

# 2. What we used to build it

I used a few main tools:

- Python for the backend
- Flask as the web framework
- SQLAlchemy to talk to the database
- SQLite as the actual database
- HTML for the structure of the pages
- CSS for styling and dark mode
- JavaScript for interactive features
- Bootstrap for layout and buttons
- Axios for sending background requests

Everything runs inside a Python virtual environment so the project has its own clean setup.

---

# 3. How the project is organized

I split the project into three main parts:

## Backend (Python + Flask)

This handles all the logic — adding games, saving ratings, searching, comparing, etc.

## Frontend (HTML + CSS + JS)

This is what the user sees — the pages, buttons, forms, dark mode, etc.

## Database (SQLite)

This stores all the information — games, ratings, tags, comments.

---

# 4. The database models (simple explanation)

## Game

A game has:

- a name
- a company
- many ratings
- many tags
- many comments

## Rating

A rating stores:

- gameplay score (1–5)
- difficulty score (1–5)
- the date
- which game it belongs to

## Tag

A tag is something like “Action”, “RPG”, “Horror”.

## Comment

A comment is just text written by the user.

---

# 5. How the backend works (`routes.py`)

## Homepage

Shows all games, their average ratings, and their tags.

## Add Game page

User enters:

- name
- company
- gameplay rating
- difficulty rating
- tags
- comment

The backend:

- creates a `Game`
- creates a `Rating`
- creates a `Comment` (if provided)
- creates `Tag` entries

## Game Detail page

Shows:

- averages
- tags
- comments

## Edit Game

Lets you change name, company, and tags.

## Delete Game

Removes the game and everything linked to it.

## Search

User types text and selects tags.

JavaScript sends a request to the backend.

Backend filters games and returns results.

## Compare

User picks two games.

Backend returns their stats side-by-side.

---

# 6. How the frontend works

## Templates (HTML + Jinja)

Each page extends a base layout.

The backend sends data into the templates.

## Tag selection

Tags are clickable chips.

When you click them, JavaScript marks them as active and stores them in a hidden input.

## Dark mode toggle

A button switches between light and dark mode.

The choice is saved in `localStorage` so it stays the same next time.

## Search and Compare

These use JavaScript + Axios to send requests without reloading the page.

---

# 7. CSS (`style.css`)

The CSS handles:

- dark mode
- light mode
- tag chip styling
- cards
- buttons
- animations
- comment boxes
- search results
- compare layout

Everything is styled to look clean and modern.

---

# 8. JavaScript (`main.js`)

The JavaScript handles:

- dark mode toggle
- tag selection
- search requests
- compare requests
- updating hidden inputs

It makes the site feel interactive and smooth.

---

# 9. How everything works together (simple explanation)

When the user does something:

1. Frontend shows a form or button
2. User interacts
3. JavaScript may update the UI or send a request
4. Backend receives the request
5. Backend updates the database
6. Backend sends data back
7. Frontend updates the page

It’s a full loop between frontend, backend, and database.
