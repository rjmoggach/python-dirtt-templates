# python-dirtt-templates

Studio project templates for [**Dirtt**](https://github.com/rjmoggach/python-dirtt)
(the Directory Tree Templater), v1.0+.

Real-world examples of describing a studio project layout as reusable
templates. Edit them to build working templates tailored to your needs.

A studio is expected to have **many job roots** and **many template sets**.
Neither is hardcoded: [`index.json`](index.json) is the registry that tooling
reads to discover what exists.

## Layout

- **`index.json`** — the registry. Every template set with its id, version,
  per-entity templates, required variables, and action counts; plus the
  job-root law. Read this first; do not hardcode template paths.
- **`studio_project_2026.05/`** — **the current set.** A hybrid AI / live
  action / design / animation / VFX studio project. Eight top-level nouns
  (`assets context lib media ref shots work` + `logs .claude`). The shot is a
  Maya-style project directory with a scene home per DCC (`c4d houdini maya
  nuke`). Six per-entity templates: project, sequence, facet (optional:
  `shots/{seq}[/{facet}]/{shot}`), shot, asset (`ref/ work/ pub/versions/`), user. Published from
  `studio-pipeline/templates/studio_project`, which is the source of truth.
- **`studio_project_2026.01/`** — superseded by 2026.05 (2026.02 facets,
  2026.03 no sequence/facet `ref/`, 2026.04 `c4d/`, 2026.05 asset `pub/versions/`). Kept so a tree stamped
  `studio_project@2026.01` can be read and migrated (`migrations/2026.01_to_2026.05.json`).
- **`studio_project_2015/`** — a VFX/post structure as deployed at a studio
  circa 2015 (`library/media/production/work/shots/flame`). Kept as a working
  historical snapshot; updated only enough to run with dirtt 1.0.
- **`migrations/`** — path maps between layouts. Keys are the old relative
  path, values the new one. Anything unlisted and unchanged matches by
  identical path; anything only in the new template is created; anything only
  in the old tree is an **orphan — kept and reported, never deleted**.

The 2026 *draft* layout (`config/io/footage/editorial/apps/deliverables`) was
replaced by `studio_project_2026.01` and is no longer shipped. It remains in
git history, and `migrations/2015_to_2026.json` is kept as a record of it.

## Job roots

A **job root** is the parent directory job directories live under. A studio
usually has several — current work, an archive volume, fast scratch, a second
facility, a client-segregated share. The `project_root` variable names one of
them at scaffold time.

Job roots are **site-local**, so their real paths live in your studio's own
config, never in this repo and never inside a project. A scaffolded project
records only the *name* of the job root it was built under
(`lib/cfg/project.json` → `job_root`), so trees stay relocatable and resolve
per platform (macOS / Linux / Windows). Nothing ever stores an absolute path.

## Usage

```console
# what can I scaffold?
python3 -c "import json;[print(s['ref'],'->',s['path']) for s in json.load(open('index.json'))['template_sets']]"

# preview — always dry-run first
dirtt create -t studio_project_2026.05/project.xml --dry-run \
    --var project_root=/Volumes/jobs --var project_dir=D26003-BIG_SUR \
    --var job_number=D26003 --var project_code=bsr \
    --var project_name=big_sur --var project_label="Big Sur" \
    --var created_by=rm

# build the project, then add entities lazily as work arrives
dirtt create -t studio_project_2026.05/sequence.xml \
    --var project_root=/Volumes/jobs --var project_dir=D26003-BIG_SUR \
    --var sequence_id=bsr010

dirtt create -t studio_project_2026.05/shot.xml \
    --var project_root=/Volumes/jobs --var project_dir=D26003-BIG_SUR \
    --var sequence_id=bsr010 --var shot=0010
```

Action counts, verified against dirtt 1.0.3:
**project 106 · sequence 3 · shot 52 · asset 3 · user 2.**

Entities are scaffolded **lazily** — one invocation per sequence, shot, asset
or artist, on first use. Never pre-create shots: a real production shipped 14
sequences with zero shot directories.

List a template's variables with:

```console
dirtt placeholders -t studio_project_2026.05/shot.xml
```

⚠️ `dirtt placeholders` does not traverse into `href`'d seed files, so it
under-reports `project.xml` (it misses `job_number`, `project_code`,
`project_name`, `project_label`, `created_by`, which are consumed by
`files/project.json` and `files/users.json`). `index.json` carries the true
variable list.

## Gotchas worth knowing before you edit a template

- dirtt substitutes `{{vars}}` inside `href`'d file **content**. If your
  wrapper pins this template set into a scaffolded project, **raw-copy** it —
  routing it through dirtt would eat the placeholders in the pinned copy.
- A literal `}}` anywhere in a template — XML comments included — is a
  `TemplateError`.
- Re-running a template over an existing tree skips directories but **refuses
  to overwrite `<file>` nodes**. Wrappers need a skip-existing pass to be
  idempotent.
- `chown` applies only when run as root; `chmod` always. A non-root scaffold
  gets correct modes and wrong owners.
- Case-only renames (`Creative` → `creative`) collide on case-insensitive
  volumes (macOS, SMB, Dropbox). Always two-step them: `X` → `X__mig` → `x`.

The Python 2 helper scripts that used to live in `scripts/` were removed; the
`dirtt` CLI replaces them.

(c) 2011–2026 Robert Moggach. MIT license.
