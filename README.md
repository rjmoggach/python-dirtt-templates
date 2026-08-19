# python-dirtt-templates

Example studio project templates for [**Dirtt**](https://github.com/rjmoggach/python-dirtt)
(the Directory Tree Templater), v1.0+.

These are real-world examples of how to describe a studio project
layout as reusable templates. Edit them to build working templates
tailored to your needs.

## Layout

- **`studio_project_2015/`** — a VFX/post project structure as deployed
  at a studio circa 2015 (library/media/production/work/shots/flame).
  Kept as a working historical snapshot; updated only enough to run
  with dirtt 1.0 (relative `href` paths).
- **`studio_project_2026/`** — the modernized layout
  (config/io/assets/footage/editorial/production/shots/work/apps/deliverables).
  Every significant directory carries a stable `id` — these ids are the
  keys migration tooling uses to track a directory across renames.
- **`migrations/2015_to_2026.json`** — the key mapping between the two
  layouts: `"old/relative/path": "new/relative/path"`. Anything not
  listed and unchanged matches by identical path; anything only in the
  new template gets created; anything only in the old tree is an orphan
  (kept, reported).

## Usage

```console
# preview
dirtt create -t studio_project_2026/project.xml \
    --var project_root=/jobs --var project_path=my_spot --dry-run

# build
dirtt create -t studio_project_2026/project.xml \
    --var project_root=/jobs --var project_path=my_spot
```

Both `project.xml` roots take the same two variables:
`project_root` (parent path, e.g. `/jobs`) and `project_path`
(project directory name). The 2015 sequence/shot/clip templates
additionally take `sequence_name`, `shot_name`, or `clip_name` —
list a template's variables with:

```console
dirtt placeholders -t studio_project_2015/project_shot.xml
```

The Python 2 helper scripts that used to live in `scripts/` were
removed; the `dirtt` CLI replaces them.

(c) 2011–2026 Robert Moggach. MIT license.
