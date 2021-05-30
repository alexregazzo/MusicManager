-- GENERAL WAY OF CHANGING DATABASE

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `playlist1`
(
    pla_id         INTEGER NOT NULL PRIMARY KEY,
    use_username   TEXT    NOT NULL,
    pla_type       TEXT    NOT NULL,
    pro_id         INTEGER NULL,
    pla_spotify_id TEXT    NULL,
    FOREIGN KEY (use_username) REFERENCES `user` (use_username)
);

INSERT INTO
    `playlist1`
SELECT
    pla_id,
    use_username,
    pla_type,
    NULL,
    pla_spotify_id
    FROM
        playlist;

DROP TABLE `playlist`;

ALTER TABLE `playlist1`
    RENAME TO `playlist`;

-- COMMIT;