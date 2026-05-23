# NP-Tennis Frontend

A terminal-based (TUI) client for the NP-Tennis court booking system, built with [Textual](https://github.com/Textualize/textual).

Browse courts, book time slots, manage orders and your profile -- all from the terminal.

## Features

- **Authentication** -- Login, register, and password reset flow with email verification; automatic token refresh on expiry
- **Court Browsing** -- Browse tennis courts with details (surface type, location, price, facility); view weekly schedules and available time slots
- **Order Management** -- Select and book consecutive time slots; view order history with booking details and time ranges
- **Profile Management** -- Edit personal information (name, email); change password with validation; export account data to JSON; delete account
- **Secure Token Storage** -- Refresh tokens persisted in the OS keyring via `keyring`; auto-refresh on 401 responses
- **Theme Support** -- Three built-in dark themes (np-tennis, np-tennis-minimal, np-tennis-alpha), switchable at runtime
- **Keyboard Navigation** -- Full keyboard-driven UI with bindings for logout, hub, profile, back, and more
- **Responsive Layout** -- Widgets adapt to terminal size (court cards collapse to compact mode on narrow terminals; forms reflow grid columns)

## Prerequisites

- Python **3.11+**
- A running NP-Tennis backend API (FastAPI)

## Installation

### 1. Create a virtual environment

**Windows:**

```bash
py -m venv .venv
```

**Linux/macOS:**

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install the package and dependencies

**Windows:**

```bash
py -m pip install -e ".[dev]"
```

**Linux/macOS:**

```bash
pip3 install -e ".[dev]"
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and adjust the values:

```env
SERVICE_NAME="NP-TENNIS"
KEY_NAME="refresh_token"
API_URL=http://localhost:8000
```

| Variable       | Description                            |
|----------------|----------------------------------------|
| `SERVICE_NAME` | Keyring service name for token storage |
| `KEY_NAME`     | Keyring key name for the refresh token |
| `API_URL`      | Base URL of the NP-Tennis backend API  |

### 5. Run the application

**Windows:**

```powershell
./tasks.ps1 run
```

**Linux/macOS:**

```bash
make run
```

### Build a standalone executable (optional)

**Windows:**

```powershell
./tasks.ps1 build
```

**Linux/macOS:**

```bash
make build
```

## Screenshots

![Main screen](README/screenshot_1.svg)
<p align="center"><em>Main screen</em></p>

![Login screen](README/screenshot_2.svg)
<p align="center"><em>Login screen</em></p>

![Register screen](README/screenshot_3.svg)
<p align="center"><em>Register screen</em></p>

![Forgot password screen](README/screenshot_4.svg)
<p align="center"><em>Forgot password screen</em></p>

![Hub screen — Courts tab](README/screenshot_5.svg)
<p align="center"><em>Hub screen — Courts tab</em></p>

![Hub screen — Orders tab](README/screenshot_6.svg)
<p align="center"><em>Hub screen — Orders tab</em></p>

![Court detail view](README/screenshot_7.svg)
<p align="center"><em>Court detail view</em></p>

![Profile — Personal Info tab](README/screenshot_8.svg)
<p align="center"><em>Profile — Personal Info tab</em></p>

![Profile — Security tab](README/screenshot_9.svg)
<p align="center"><em>Profile — Security tab</em></p>

![Export data modal](README/screenshot_10.svg)
<p align="center"><em>Export data modal</em></p>

## Project Structure

```
frontend/
├── .env.example              # Environment variable template
├── build.py                  # PyInstaller build script
├── Makefile                  # Linux/macOS task runner
├── tasks.ps1                 # Windows PowerShell task runner
├── NP-Tennis.spec            # PyInstaller spec
├── pyproject.toml            # Project metadata, dependencies, tooling config
├── styles/                   # Textual CSS stylesheets (*.tcss)
│   ├── styles.tcss
│   ├── buttons.tcss
│   ├── header.tcss
│   ├── main_screen.tcss
│   ├── login_screen.tcss
│   ├── register_screen.tcss
│   ├── forgot_password_screen.tcss
│   ├── hub_screen.tcss
│   ├── profile_screen.tcss
│   ├── modals.tcss
│   ├── courts.tcss
│   └── views.tcss
├── README/                   # Screenshots
├── uml/                      # UML diagrams
└── src/tuiapp/               # Application package
    ├── __init__.py
    ├── main.py               # Entry point
    ├── app.py                # TUIApplication (root App class)
    ├── settings.py           # Pydantic-settings configuration
    ├── themes.py             # Theme definitions
    ├── time_utils.py         # Timezone conversion helpers
    ├── api/                  # Backend API layer
    │   ├── client.py         # Async HTTP client (httpx)
    │   ├── errors.py         # APIError exception
    │   ├── schema.py         # Common schemas (Result, Message)
    │   ├── auth/
    │   │   ├── auth.py         # AuthService (login, register, password reset)
    │   │   ├── auth_guard.py   # AuthGuard mixin
    │   │   ├── schema.py       # Auth Pydantic models
    │   │   └── token_manager.py # Token persistence & refresh
    │   ├── account/
    │   │   ├── account.py      # AccountService (profile, password, export, delete)
    │   │   └── schema.py       # Account Pydantic models
    │   ├── court/
    │   │   ├── court.py        # CourtService (list, schedule, available slots)
    │   │   └── schema.py       # Court Pydantic models
    │   ├── order/
    │   │   ├── order.py        # OrderService (list, detail, create)
    │   │   └── schema.py       # Order Pydantic models
    │   └── status/
    │       ├── status.py       # StatusService
    │       └── schema.py       # Status Pydantic models
    ├── screens/              # Top-level screens
    │   ├── base_screen.py    # BaseScreen, AuthScreen
    │   ├── main_screen.py    # Landing screen (Login / Signup)
    │   ├── login_screen.py   # Login form screen
    │   ├── register_screen.py # Registration form screen
    │   ├── forgot_password_screen.py # Password reset flow
    │   ├── hub_screen.py     # Main dashboard (Courts / Orders tabs)
    │   └── profile_screen.py # Profile / Security tabs
    └── widgets/              # Reusable UI components
        ├── buttons.py        # Primary, Secondary, Danger buttons
        ├── header.py         # Custom header with navigation
        ├── inputs.py         # TextInput, PasswordInput, CodeInput, etc.
        ├── courts/
        │   ├── card_container.py # Scrollable vertical card list
        │   ├── court_card.py   # Court summary card
        │   └── schedule_slot.py # Bookable time slot widget
        ├── forms/
        │   ├── base_form.py    # Base form with validation
        │   ├── login_form.py   # Login form fields
        │   ├── register_form.py # Registration form fields
        │   ├── forgot_password_form.py # Email input form
        │   └── new_password_form.py   # New password form
        ├── modals/
        │   ├── base_modal.py          # BaseModal with overlay
        │   ├── confirmation_modal.py  # Yes/No confirmation dialog
        │   ├── delete_account_modal.py # Account deletion confirmation
        │   ├── export_data_modal.py   # File export with directory picker
        │   ├── password_hints_modal.py # Password requirements display
        │   └── status_modal.py        # Status information modal
        ├── order/
        │   └── order_card.py  # Order summary card
        └── views/
            ├── base_view.py    # Abstract view base class
            ├── court_view.py   # Court detail / schedule / booking view
            ├── order_view.py   # Order detail view
            ├── personal_information_view.py # Edit name / export data
            └── security_view.py # Change password / delete account
```

## Tech Stack

| Layer         | Technology                                                                        |
|---------------|-----------------------------------------------------------------------------------|
| Framework     | [Textual](https://github.com/Textualize/textual) >= 0.50                          |
| HTTP Client   | [httpx](https://www.python-httpx.org/) >= 0.27                                    |
| Validation    | [Pydantic](https://docs.pydantic.dev/) >= 2.0                                     |
| Settings      | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| Keyring       | [keyring](https://github.com/jaraco/keyring) >= 25.7                              |
| Linting       | Ruff, mypy                                                                        |
| Testing       | pytest, pytest-asyncio                                                            |
| Packaging     | setuptools, PyInstaller (optional)                                                |

## License

[MIT](LICENSE)
