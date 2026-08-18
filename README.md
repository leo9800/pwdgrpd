# pwdgrpd

**pwdgrpd** (Password & Group Daemon) is a RESTful API server written in Python and FastAPI that serves Unix `/etc/passwd` and `/etc/group` information over HTTP. It provides standard POSIX user/group lookups (`getpwnam`, `getpwuid`, `getgrnam`, `getgrgid`, `initgroups`, etc.) returning either structured JSON or standard raw Unix format strings.

---

## Features

* **POSIX Standard Endpoints**: Look up users and groups by name or ID.
* **Dual Output Formats**: Supports responses in both `json` and `raw` (colon-delimited Unix text format).
* **Flexible Data Sources**: Load user/group data directly from standard Unix text files (`/etc/passwd`, `/etc/group`) or a pre-compiled JSON file.
* **Security Control**: Disable full enumeration (`/getpwall`, `/getgrall`) via configuration to prevent full database dumps.
* **High Performance**: Built on FastAPI, Pydantic v2, and Uvicorn.

---

## Installation

### Prerequisites

* Python 3.12 or higher

### Install via Pip

```bash
pip install .

```

For development and testing dependencies:

```bash
pip install .[test]

```

---

## Configuration

Configuration can be set via environment variables (prefixed with `PWDGRPD_`) or via a `.env` file in the project directory.

| Variable | Type | Default | Description |
| --- | --- | --- | --- |
| `PWDGRPD_HOST` | `str` | `0.0.0.0` | Bind host address |
| `PWDGRPD_PORT` | `int` | `8000` | Bind port |
| `PWDGRPD_WORKERS` | `int` | `1` | Number of Uvicorn worker processes |
| `PWDGRPD_SOURCE` | `raw` | `json` | `raw` | Data source backend (`raw` file pair or `json` file) |
| `PWDGRPD_PASSWD_FILE` | `str` | `None` | Path to Unix passwd file (required if `SOURCE=raw`) |
| `PWDGRPD_GROUP_FILE` | `str` | `None` | Path to Unix group file (required if `SOURCE=raw`) |
| `PWDGRPD_JSON_FILE` | `str` | `None` | Path to JSON database file (required if `SOURCE=json`) |
| `PWDGRPD_ALLOW_ENUMERATION` | `bool` | `False` | Allow endpoints listing all entries (`/getpwall`, `/getgrall`) |
| `PWDGRPD_PROXY_HEADERS` | `bool` | `False` | Enable/disable proxy headers in Uvicorn |
| `PWDGRPD_FORWARDED_ALLOW_IPS` | `str` | `list` | `127.0.0.1` | Allowed IPs for proxy headers |

### Example `.env` Configuration

```env
PWDGRPD_HOST=127.0.0.1
PWDGRPD_PORT=8080
PWDGRPD_SOURCE=raw
PWDGRPD_PASSWD_FILE=/etc/passwd
PWDGRPD_GROUP_FILE=/etc/group
PWDGRPD_ALLOW_ENUMERATION=true
```

---

## Usage

### Starting the Server

Once installed, start the server using the CLI script:

```bash
pwdgrpd
```

Or run it directly via Python:

```bash
python -m pwdgrpd.main
```

---

## API Reference

All endpoints accept a `type` query parameter (`json` or `raw`, defaulting to `json`).

### User Endpoints (`/etc/passwd`)

| Endpoint | Query Params | Description |
| --- | --- | --- |
| `GET /getpwnam/{name}` | `type=json|raw` | Fetch a user entry by username. |
| `GET /getpwuid/{uid}` | `type=json|raw` | Fetch a user entry by UID. |
| `GET /getpwall` | `type=json|raw` | List all users. *(Requires `PWDGRPD_ALLOW_ENUMERATION=true`)* |

**Example Response (`GET /getpwnam/root?type=json`):**

```json
{
  "pw_name": "root",
  "pw_passwd": "x",
  "pw_uid": 0,
  "pw_gid": 0,
  "pw_gecos": "root",
  "pw_dir": "/root",
  "pw_shell": "/bin/bash"
}
```

**Example Response (`GET /getpwnam/root?type=raw`):**

```text
root:x:0:0:root:/root:/bin/bash
```

---

### Group Endpoints (`/etc/group`)

| Endpoint | Query Params | Description |
| --- | --- | --- |
| `GET /getgrnam/{name}` | `type=json|raw` | Fetch a group entry by group name. |
| `GET /getgrgid/{gid}` | `type=json|raw` | Fetch a group entry by GID. |
| `GET /getgrall` | `type=json|raw` | List all groups. *(Requires `PWDGRPD_ALLOW_ENUMERATION=true`)* |

---

### Supplementary Groups

| Endpoint | Query Params | Description |
| --- | --- | --- |
| `GET /initgroups/{name}` | `b=nam|gid`<br>

<br>`type=json|raw` | Fetch all additional groups a user belongs to. `b` selects whether to return names or GIDs. |

**Example (`GET /initgroups/john?b=nam&type=json`):**

```json
["sudo", "docker", "wheel"]
```

**Example (`GET /initgroups/john?b=gid&type=raw`):**

```text
27,999,10

```

---

## License

Distributed under the [GPL-3.0-or-later](https://www.google.com/search?q=LICENSE) License.