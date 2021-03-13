CREATE TABLE IF NOT EXISTS `user`
(
    use_username         TEXT NOT NULL PRIMARY KEY,
    use_email            TEXT NULL,
    use_password_salt    TEXT NOT NULL,
    use_password         TEXT NOT NULL,
    use_created_datetime TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tokenspotify
(
    use_username              TEXT    NOT NULL PRIMARY KEY,
    tok_user_spotify_id       TEXT    NULL,
    tok_access_token          TEXT    NOT NULL,
    tok_token_type            TEXT    NOT NULL,
    tok_scope                 TEXT    NOT NULL,
    tok_expires_in            INTEGER NOT NULL,
    tok_refresh_token         TEXT    NOT NULL,
    tok_last_updated_datetime TEXT    NOT NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);

CREATE TABLE IF NOT EXISTS `tokenapp`
(
    tok_id               INTEGER NOT NULL PRIMARY KEY,
    use_username         TEXT    NOT NULL,
    tok_access_token     TEXT    NOT NULL UNIQUE,
    tok_active           INTEGER NOT NULL,
    tok_created_datetime TEXT    NOT NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);



CREATE TABLE IF NOT EXISTS `run`
(
    run_id         INTEGER NOT NULL PRIMARY KEY,
    use_username   TEXT    NOT NULL,
    run_type       TEXT    NOT NULL,
    run_success    INTEGER NOT NULL,
    run_message    TEXT    NULL,
    run_error_type TEXT    NULL,
    run_traceback  TEXT    NULL,
    run_datetime   TEXT    NOT NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);

CREATE TABLE IF NOT EXISTS `artist`
(
    art_id   TEXT NOT NULL PRIMARY KEY,
    art_href TEXT NOT NULL,
    art_name TEXT NOT NULL,
    art_uri  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `album`
(
    alb_id   TEXT NOT NULL PRIMARY KEY,
    alb_href TEXT NOT NULL,
    alb_name TEXT NOT NULL,
    alb_uri  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `track`
(
    tra_id          TEXT    NOT NULL PRIMARY KEY,
    tra_duration_ms INTEGER NOT NULL,
    tra_href        TEXT    NOT NULL,
    tra_name        TEXT    NOT NULL,
    tra_preview_url TEXT    NOT NULL,
    tra_uri         TEXT    NOT NULL,
    alb_id          TEXT    NULL,
    FOREIGN KEY (alb_id) REFERENCES `album` (alb_id)
);

CREATE TABLE IF NOT EXISTS `album_image`
(
    albima_url    TEXT    NOT NULL PRIMARY KEY,
    alb_id        TEXT    NOT NULL,
    albima_width  INTEGER NULL,
    albima_height INTEGER NULL,

    FOREIGN KEY (alb_id) REFERENCES `album` (alb_id)
);


CREATE TABLE IF NOT EXISTS `track_artist`
(
    traart_id INTEGER NOT NULL PRIMARY KEY,
    tra_id    TEXT    NOT NULL,
    art_id    TEXT    NOT NULL,
    FOREIGN KEY (tra_id) REFERENCES `track` (tra_id),
    FOREIGN KEY (art_id) REFERENCES `artist` (art_id)
);

CREATE TABLE IF NOT EXISTS `history`
(
    his_id        INTEGER NOT NULL PRIMARY KEY,
    use_username  INTEGER NOT NULL,
    tra_id        INTEGER NOT NULL,
    his_played_at TEXT    NOT NULL,
    FOREIGN KEY (tra_id) REFERENCES `track` (tra_id),
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);

CREATE TABLE IF NOT EXISTS `playlist`
(
    pla_id         INTEGER NOT NULL PRIMARY KEY,
    use_username   TEXT    NOT NULL,
    pla_type       TEXT    NOT NULL,
    pla_spotify_id TEXT    NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);


CREATE TABLE IF NOT EXISTS `notification`
(
    not_id       INTEGER NOT NULL PRIMARY KEY,
    use_username TEXT    NOT NULL,
    not_type     TEXT    NOT NULL,
    not_done     INTEGER NOT NULL,
    not_message  TEXT    NOT NULL,
    not_datetime TEXT    NOT NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);



