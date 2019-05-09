-- players table
CREATE TABLE IF NOT EXISTS players (
    id integer PRIMARY KEY,
    nickname text NOT NULL,
    discord_id text NOT NULL
);

-- characters table
CREATE TABLE IF NOT EXISTS characters (
    id integer PRIMARY KEY,
    name text NOT NULL,
    player_id integer NOT NULL,
    level integer,
    strength integer,
    dextery integer,
    intelligence integer,
    constitution integer,
    wisdom integer,
    carisma integer,
    armor integer,
    current_xp integer,
    current_hp integer,
    max_hp integer,
    FOREIGN KEY (player_id) REFERENCES players (id)
);

-- expertise X character relation table
CREATE TABLE IF NOT EXISTS  char_expertises (
    id integer PRIMARY KEY,
    char_id integer NOT NULL,
    expertise text,
    FOREIGN KEY (char_id) REFERENCES characters (id)
);

-- skill X character relation table
CREATE TABLE IF NOT EXISTS  char_skills (
    id integer PRIMARY KEY,
    char_id integer NOT NULL,
    skill text,
    FOREIGN KEY (char_id) REFERENCES characters (id)
);

-- spells X character relation table
CREATE TABLE IF NOT EXISTS  char_spells (
    id integer PRIMARY KEY,
    char_id integer NOT NULL,
    spell text,
    FOREIGN KEY (char_id) REFERENCES characters (id)
);

-- talentes X character relation table
CREATE TABLE IF NOT EXISTS  char_talentes (
    id integer PRIMARY KEY,
    char_id integer NOT NULL,
    talent text,
    FOREIGN KEY (char_id) REFERENCES characters (id)
);

-- class level X character relation table
CREATE TABLE IF NOT EXISTS  char_class_levels (
    id integer PRIMARY KEY,
    char_id integer NOT NULL,
    class text,
    class_level integer, 
    FOREIGN KEY (char_id) REFERENCES characters (id)
);

-- End of character related stuff

-- monster table
CREATE TABLE IF NOT EXISTS  monsters (
    id integer PRIMARY KEY,
    ND integer NOT NULL,
    name text,
    armor integer,
    max_hp integer,
    current_hp integer 
);

-- monster X attack relational table
CREATE TABLE IF NOT EXISTS  monster_attack (
    id integer PRIMARY KEY,
    monster_id integer NOT NULL,
    attack text,
    attack_name text, 
    FOREIGN KEY (monster_id) REFERENCES monsters (id)
);