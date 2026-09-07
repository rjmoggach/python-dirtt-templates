# lib/dirtt — this project's structural map

This folder carries the dirtt template set that BUILT this project, so the project
knows its own structure and can be re-mapped or migrated later.

Contents (populated by the scaffold wrapper):
  project.xml, sequence.xml, shot.xml, asset.xml, user.xml   the template set, pinned at scaffold time
  files/                                                     seed files (workspace.mel, ...)
  scaffold.log.jsonl                                         every scaffold run: template@version, vars, date, actor
  migrations/                                                mapping files when this project moves to a newer structure

Why here: a year from now, any tool (or person) can read this folder and know exactly
which structure governs this tree — and diff it against the studio's current template
to plan a migration.

Caution law:
  - the templates here are a RECORD; applying them is always dry-run first
  - migration mappings are proposed, reviewed, then applied; orphans are kept and
    reported, never deleted
  - case-only renames go two-step (x -> x_tmp -> X); assume case-insensitive volumes
