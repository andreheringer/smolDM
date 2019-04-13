-- players table
CREATE TABLE IF NOT EXISTS players (
    id integer PRIMARY KEY,
    name text NOT NULL,
    discord_id text NOT NULL
);

-- characters table
CREATE TABLE IF NOT EXISTS characters (
    id integer PRIMARY KEY,
    name text NOT NULL,
    player_id integer NOT NULL,
    char_class text,
    char_level integer,
    strength integer,
    dextery integer.
    intelligence integer,
    constitution integer,
    wisdom integer,
    carisma integer,
    armor integer,
    talents text,
    current_xp integer,
    expertise text,
    skills text,
    current_hp integer,
    max_hp integer,
    spells text
);