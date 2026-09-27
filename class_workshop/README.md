# Time Complexity Visualizer — Class Workshop

A set of small Flask APIs that empirically measure how an algorithm's running
time scales with input size, plot the result with matplotlib, return the chart
as base64, and (optionally) persist each analysis to a SQLite database.

Three runnable variants live side by side in this folder — pick the one that
matches what you want to demo:

| Variant | File | Algorithms | Extras |
|---|---|---|---|
| **Main app** | [`app.py`](app.py) | 4 (search/sort + nested loops) | Annotated chart, `total_time_ms`, DB save, host `0.0.0.0` |
| **Full suite** | [`visualize.py`](visualize.py) | 6 (adds `insertion_sort`, `selection_sort`) | Raw timing series + `image_path` in the response |
| **Stack & queue** | [`visualize_with_stack&queue.py`](visualize_with_stack&queue.py) | 12 (adds 6 stack/queue operations) | Uses [`stack.py`](stack.py) / [`queue.py`](queue.py) as measured data structures |

## Contents

- [How it works](#how-it-works)
- [Project layout](#project-layout)
- [Requirements](#requirements)
- [Running the server](#running-the-server)
- [API reference](#api-reference)
  - [`GET /analyze`](#get-analyze)
  - [`POST /save_analysis`](#post-save_analysis)
- [Supported algorithms](#supported-algorithms)
- [Stack and queue operations](#stack-and-queue-operations)
- [Database](#database)
- [Snapshots](#snapshots)
- [Tests](#tests)
- [Adding a new algorithm](#adding-a-new-algorithm)
- [Known limitations](#known-limitations)

## How it works

For a request like `algo=linear_search&step=100&n_max=10000`, the server:

1. Builds a list of input sizes `0, step, 2*step, ..., n_max`
   (`n_min` is hard-coded to `0` in every variant).
2. Runs the chosen algorithm once per input size, timing each run with
   `time.perf_counter()` (`time.time()` in `app.py`).
3. Plots input size (x-axis) against running time in seconds (y-axis) with
   matplotlib, using the non-interactive `Agg` backend so it can run headless
   on a server with no display.
4. Saves the plot as a PNG (`static/snapshots/` in `app.py`, `snapshots/` in
   the other two variants).
5. Returns the chart as base64 in the JSON response — along with the raw
   timing series in `visualize*.py`, or derived fields such as
   `time_complexity` and `total_time_ms` in `app.py`.

## Project layout

| File | Responsibility |
|---|---|
| [`app.py`](app.py) | Main Flask app. `/analyze` + `/save_analysis`, 4 algorithms, pretty-printed complexity labels, snapshots written to `static/snapshots/`. |
| [`visualize.py`](visualize.py) | Standalone Flask app with 6 algorithms and a more detailed `/analyze` response (`input_sizes`, `times`, `image_path`). |
| [`visualize_with_stack&queue.py`](visualize_with_stack&queue.py) | Same as `visualize.py` plus 6 stack/queue benchmarks (12 algorithms total). |
| [`stack.py`](stack.py) | List-based `Stack` (`push`, `pop`, `peek`, `is_empty`, `size`). |
| [`queue.py`](queue.py) | List-based `Queue` (`enqueue`, `dequeue`, `peek`, `is_empty`, `size`). |
| [`testing_stack.py`](testing_stack.py) | `unittest` suite for `Stack` (7 tests). |
| [`testing_queue.py`](testing_queue.py) | `unittest` suite for `Queue` (7 tests). |
| [`database.py`](database.py) | Flask-SQLAlchemy `Analysis` model — one row per saved analysis. |
| [`essential_req.txt`](essential_req.txt) | Pinned `pip` dependencies. |
| `snapshots/`, `static/snapshots/` | Generated PNG charts (created on first run, in the directory you launch from). |
| `instance/analysis.db` | SQLite database (created on first run, in the directory you launch from). |

## Requirements

- Python 3.10+
- `flask`, `matplotlib`, `numpy`
- `Flask-SQLAlchemy` (for `app.py`, `visualize.py`, `visualize_with_stack&queue.py`)

Install with:

```bash
source ../.venv/bin/activate
pip install -r essential_req.txt
pip install Flask-SQLAlchemy
```

> Always activate the project venv first (`source ../.venv/bin/activate` from
> this folder). Plain `python` is not on PATH on a fresh shell, and the system
> `python3` has no Flask installed. The venv already contains every pinned
> dependency plus `Flask-SQLAlchemy`.

## Running the server

From this directory (venv activated):

```bash
source ../.venv/bin/activate
python app.py            # main app   -> http://localhost:8000  (all interfaces)
python visualize.py      # 6 algorithms
python "visualize_with_stack&queue.py"   # 12 algorithms incl. stack/queue
```

Only one of them can run at a time — they all bind to port `8000`. Debug mode
is on, so each app auto-reloads when you edit its source. Stop it with
`Ctrl+C` in that terminal.

Try it:

```
GET http://localhost:8000/analyze?algo=linear_search&step=100&n_max=10000
```

## API reference

The endpoints below are shared by `app.py`, `visualize.py`, and
`visualize_with_stack&queue.py`. Response fields differ slightly per variant —
differences are called out inline.

### `GET /analyze`

Runs one algorithm across a range of input sizes and returns timing data plus
a chart.

**Query parameters**

| Name | Type | Required | Notes |
|---|---|---|---|
| `algo` | string | Yes | One of the [supported algorithms](#supported-algorithms). The `visualize*` variants strip surrounding quotes, so `algo='linear_search'` and `algo=linear_search` are equivalent; `app.py` does **not** strip quotes. |
| `step` | integer | Yes | Spacing between successive input sizes. `app.py` defaults to `100` when omitted; the `visualize*` variants return `400`. |
| `n_max` | integer | Yes | Upper bound on input size. `app.py` defaults to `10000` when omitted; the `visualize*` variants return `400`. |

`n_min` is implicit and always `0`.

**Example response** (`200 OK`)

`app.py` — derived fields and a data-URI image:

```json
{
  "algo": "Linear Search",
  "end_time": 1790542130,
  "graph_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...",
  "items": 10000,
  "start_time": 1790542120,
  "steps": 100,
  "time_complexity": "O(n)",
  "total_time_ms": 183
}
```

`visualize.py` / `visualize_with_stack&queue.py` — raw series and a plain
base64 image:

```json
{
  "algorithm": "linear_search",
  "n_min": 0,
  "n_max": 10000,
  "step": 100,
  "input_sizes": [0, 100, 200, ..., 10000],
  "times": [0.0000012, 0.0000431, ...],
  "image_path": "snapshots/linear_search.png",
  "image_base64": "iVBORw0KGgoAAAANSUhEUgA..."
}
```

`image_base64` is a raw base64-encoded PNG — decode it directly to bytes and
write to a `.png` file, or prefix it with `data:image/png;base64,` to embed it
in an `<img>` tag or Markdown. `app.py` already returns it with that prefix as
`graph_base64`.

**Error responses** (`400 Bad Request`)

| Condition | Body |
|---|---|
| `algo` missing | `{"error": "Please provide algo, step and n_max"}` (`visualize*`) — `app.py` instead reports `Algorithm "None" not supported. ...` |
| `algo` not recognized | `{"error": "Unknown algorithm", "available_algorithms": [...]}` (`visualize*`) or `{"error": "Algorithm \"<value>\" not supported. Available algorithms: [...]"}` (`app.py`) |
| `step` / `n_max` non-integer | `{"error": "step and n_max must be integers"}` (`visualize*`) or `{"error": "Invalid step or n_max value. Please provide valid integers."}` (`app.py`) |
| `step` ≤ 0 | `{"error": "step must be greater than 0"}` (`visualize*`); `app.py` does not check this |
| `n_max` < 0 | `{"error": "n_max must be greater than or equal to 0"}` (`visualize*`); `app.py` does not check this |

### `POST /save_analysis`

Persists one analysis to SQLite (table `analysis`). Accepts a JSON body.

**Required fields**

| Field | Type |
|---|---|
| `algorithm` | string |
| `n_min`, `n_max`, `step` | integer |
| `input_sizes`, `times` | array of numbers (stored as JSON text) |
| `image_path` | string |

**Responses**

- `201` — `{"message": "Analysis saved successfully", "analysis_id": 1}`
- `400` — `{"error": "Please provide JSON data"}` or `{"error": "Missing field: <name>"}`

## Supported algorithms

Each algorithm is a plain function `f(n)` that performs one run on an input of
size `n`. Sorting algorithms operate on a reverse-sorted list (worst case).

| `algo` value | Available in | Description | Expected time complexity |
|---|---|---|---|
| `linear_search` | all | Linear scan of `n` elements. | O(n) |
| `binary_search` | all | Binary search over `0..n-1` for the last element. | O(log n) |
| `bubble_sort` | all | Bubble sort on a reverse-sorted list. In `app.py` the list is capped at 1000 elements. | O(n²) |
| `nested_loops` | all | Two nested `range(n)` loops. In `app.py` capped at 500. | O(n²) |
| `insertion_sort` | `visualize.py`, `visualize_with_stack&queue.py` | Insertion sort on a reverse-sorted list. | O(n²) |
| `selection_sort` | `visualize.py`, `visualize_with_stack&queue.py` | Selection sort on a reverse-sorted list. | O(n²) |

`app.py` also labels each result with its complexity via the `COMPLEXITIES`
map, shown as `time_complexity` in the response.

## Stack and queue operations

[`visualize_with_stack&queue.py`](visualize_with_stack&queue.py) additionally
benchmarks operations on the workshop's own data structures:

| `algo` value | Description | Expected time complexity |
|---|---|---|
| `stack_push` | `push` `n` items onto a fresh `Stack`. | O(n) |
| `stack_pop` | Fill with `n` items, then `pop` them all. | O(n) |
| `stack_peek` | Fill with `n` items, then call `peek` `n` times. | O(n) |
| `queue_enqueue` | `enqueue` `n` items onto a fresh `Queue`. | O(n) |
| `queue_dequeue` | Fill with `n` items, then `dequeue` them all. | O(n²) — `list.pop(0)` is O(n) per call |
| `queue_peek` | Fill with `n` items, then call `peek` `n` times. | O(n) |

The list-backed `Queue.dequeue` shifting behaviour is a nice classroom
demonstration of why a `collections.deque` is preferred in practice.

## Database

- Engine: SQLite via Flask-SQLAlchemy — configured as `sqlite:///analysis.db`
  and resolved against the app's **instance folder**, which Flask places at
  `instance/` inside the directory you launch the server from (run it from
  this folder → `class_workshop/instance/analysis.db`).
- Model: [`database.py`](database.py) → class `Analysis`
  (`id`, `algorithm`, `n_min`, `n_max`, `step`, `input_sizes`, `times`,
  `image_path`, `created_at`).
- Tables are created automatically at startup (`db.create_all()` inside an
  app context).

Note that `/analyze` itself does **not** write to the database — only
`POST /save_analysis` does. Note also that `app.py`'s `/analyze` response does
**not** contain `input_sizes`, `times`, or `image_path`, so its output can't be
forwarded as-is; you must assemble the body yourself (the `visualize*`
variants do return those fields and can be passed through directly).

## Snapshots

| File | Location | Naming |
|---|---|---|
| `app.py` | `static/snapshots/` | `snapshot_<unix-epoch>.png` |
| `visualize.py`, `visualize_with_stack&queue.py` | `snapshots/` | `<algorithm_name>.png` (overwritten each run) |

Directories are created automatically on first run, relative to the directory
you launch the server from. The same image is also returned inline in the
response, so the file on disk is a persistent copy / audit trail rather than
something the caller must read to get the chart.

## Tests

Unit tests cover the `Stack` and `Queue` implementations (empty checks,
push/pop, peek, LIFO/FIFO ordering, and `IndexError` on empty structures):

```bash
python -m unittest testing_stack testing_queue -v
```

Or run each file directly:

```bash
python testing_stack.py
python testing_queue.py
```

Both currently pass: **14 tests, 0 failures**.

## Adding a new algorithm

1. Define a function with the signature `def my_algorithm(n): ...` that does
   one full run for input size `n` (avoid work that grows much faster than
   the algorithm under test, or cap `n` like `bubble_sort` does).
2. Register it in the `algorithms` dict (`visualize*.py`) or `ALGOS` dict
   (`app.py`) with the key you want exposed as the `algo` query value:

   ```python
   algorithms = {
       ...
       "my_algorithm": my_algorithm,
   }
   ```

3. If the variant labels complexity (`app.py`), add an entry to
   `COMPLEXITIES` and `PRETTY_NAMES`.
4. No route changes are needed — `/analyze` reads from the dict dynamically.

To benchmark a new data structure, add the structure in `stack.py` / `queue.py`
(or a new module), write a `f(n)` wrapper, and register it the same way.

## Known limitations

- Timing uses wall-clock/`perf_counter` around a **single run** per input
  size — no repetition or averaging, so results are noisy for very small `n`
  or on a busy machine. Use a larger `step`/`n_max` range where runtime
  dominates measurement overhead.
- O(n²) algorithms (`bubble_sort`, `nested_loops`, `insertion_sort`,
  `selection_sort`) with a large `n_max` can make a single request take a long
  time, since the server runs the algorithm once per input size synchronously
  before responding.
- `app.py` caps `bubble_sort` at 1000 elements and `nested_loops` at 500, so
  their curves flatten out past those sizes — intentional, to keep requests
  fast, but worth knowing when interpreting the plot.
- The local module `queue.py` shadows the standard-library `queue` module.
  That's fine here (the local one is what's wanted), but anything expecting
  `queue.Queue`/`queue.Empty` from the stdlib won't work inside this folder.
- All three servers hard-code port `8000` and run with `debug=True` — fine
  for local development, not for anything exposed beyond `localhost`.
