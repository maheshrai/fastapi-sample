# Electric Utility API

A FastAPI-based REST API for electric utility operations including customer lookup, meter data, usage history, billing, and outage management.

Customer and outage services use Faker for mock data. Billing connects to Oracle Autonomous Database via wallet.

## Project Structure

```
fastapi-sample/
├── main.py                        # App entry point
├── config.py                      # Settings loaded from .env
├── db.py                          # Oracle connection pool (lazy init)
│
├── models/
│   ├── customer.py                # Customer, Meter, UsageRecord
│   ├── billing.py                 # Bill, Payment, PaymentRequest
│   └── outage.py                  # Outage, OutageReport
│
├── routers/
│   ├── customers.py               # /customers routes
│   ├── billing.py                 # /customers/{id}/bills, /payments routes
│   └── outages.py                 # /outages routes
│
└── services/
    ├── customer_service.py        # Faker-based mock
    ├── billing_service.py         # Oracle DB
    └── outage_service.py          # Faker-based mock
```

## Setup

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your Oracle Autonomous Database credentials:

```env
ORACLE_DB_USER=admin
ORACLE_DB_PASSWORD=your_password
ORACLE_DB_DSN=mydb_high          # TNS alias from tnsnames.ora in the wallet
ORACLE_WALLET_DIR=/path/to/wallet
ORACLE_WALLET_PASSWORD=          # Leave blank for SSO wallets
```

The wallet directory should be the unzipped contents of the wallet zip downloaded from the OCI console. It must contain `cwallet.sso`, `tnsnames.ora`, and `sqlnet.ora`.

### 3. Run

```bash
uvicorn main:app --reload
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## API Endpoints

### Customers
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/customers` | List customers (`?name=`, `?status=`, `?limit=`) |
| `GET` | `/customers/{account_number}` | Get customer by account number |
| `GET` | `/customers/{account_number}/meter` | Get meter details |
| `GET` | `/customers/{account_number}/usage` | Get usage history (`?months=12`) |

### Billing
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/customers/{account_number}/bills` | Get bill history (`?limit=12`) |
| `GET` | `/customers/{account_number}/bills/{bill_id}` | Get a specific bill |
| `POST` | `/customers/{account_number}/payments` | Submit a payment |

### Outages
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/outages` | List outages (`?status=`, `?zip_code=`) |
| `GET` | `/outages/{outage_id}` | Get outage details |
| `POST` | `/outages` | Report a new outage |

## Mock Data

Customer and outage endpoints return Faker-generated data seeded by account/outage ID, so responses are consistent across restarts.

- 20 pre-seeded customers: `ELEC-000001` through `ELEC-000020`
- 10 pre-seeded outages: `OUT-00001` through `OUT-00010`

## Adding a New Domain

1. Add models to `models/<domain>.py`
2. Add business logic to `services/<domain>_service.py`
3. Add routes to `routers/<domain>.py`
4. Register the router in `main.py`:
   ```python
   app.include_router(<domain>.router)
   ```
