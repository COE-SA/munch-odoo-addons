# -*- coding: utf-8 -*-
"""Build a complete, monthly financial history from Odoo.

The report closes on the last day of the previous calendar month.  This keeps
partial-month postings out of executive comparisons while retaining every
closed month since the first posted P&L entry.
"""
import json
import os
import xmlrpc.client
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlsplit

raw_url = os.environ["ODOO_URL"].strip().strip("'\"")
if raw_url.upper().startswith("ODOO_URL="):
    raw_url = raw_url.split("=", 1)[1].strip().strip("'\"")
if not raw_url.startswith(("http://", "https://")):
    raw_url = f"https://{raw_url}"
parsed_url = urlsplit(raw_url)
if not parsed_url.hostname:
    raise SystemExit("ODOO_URL does not contain a valid hostname")
URL = f"{parsed_url.scheme}://{parsed_url.netloc}".rstrip("/")
DB = os.environ["ODOO_DB"]
USER = os.environ["ODOO_USER"]
KEY = os.environ["ODOO_API_KEY"]
RIYADH = timezone(timedelta(hours=3))

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common", allow_none=True)
uid = common.authenticate(DB, USER, KEY, {})
if not uid:
    raise SystemExit("Odoo authentication failed")
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object", allow_none=True)


def call(model, method, args, kwargs=None):
    return models.execute_kw(DB, uid, KEY, model, method, args, kwargs or {})


def paged(model, domain, fields, order="id asc", limit=5000):
    rows, offset = [], 0
    while True:
        batch = call(model, "search_read", [domain], {
            "fields": fields, "limit": limit, "offset": offset, "order": order,
        })
        rows.extend(batch)
        if len(batch) < limit:
            return rows
        offset += len(batch)


def month_key(value):
    return str(value)[:7]


def add_amount(target, key, amount):
    target[key] = target.get(key, 0.0) + float(amount or 0.0)


today = datetime.now(RIYADH).date()
period_end = today.replace(day=1) - timedelta(days=1)
period_end_s = period_end.isoformat()

accounts = paged("account.account", [], ["id", "code", "name", "account_type"])
account_map = {a["id"]: a for a in accounts}
pnl_ids = [a["id"] for a in accounts if a.get("account_type") in {
    "income", "income_other", "expense", "expense_direct_cost", "expense_depreciation"
}]
if not pnl_ids:
    raise SystemExit("No P&L accounts are visible to this Odoo user")

first_rows = call("account.move.line", "search_read", [[
    ["move_id.state", "=", "posted"], ["account_id", "in", pnl_ids],
    ["date", "<=", period_end_s],
]], {"fields": ["date"], "limit": 1, "order": "date asc,id asc"})
if not first_rows:
    raise SystemExit("No posted P&L entries were found")
earliest = str(first_rows[0]["date"])

lines = paged("account.move.line", [
    ["move_id.state", "=", "posted"], ["account_id", "in", pnl_ids],
    ["date", ">=", earliest], ["date", "<=", period_end_s],
], ["date", "account_id", "balance", "debit", "credit", "name"])

monthly = defaultdict(lambda: {
    "revenue": 0.0, "cogs": 0.0, "opex": 0.0, "net_profit": 0.0,
    "expenses": defaultdict(float),
})


def expense_bucket(account):
    text = (str(account.get("name", "")) + " " + str(account.get("code", ""))).lower()
    groups = [
        ("rent", ("rent", "rental", "lease", "إيجار")),
        ("salaries", ("salary", "salar", "wage", "payroll", "رواتب", "راتب")),
        ("delivery", ("delivery", "commission", "توصيل", "عمولة")),
        ("royalty", ("royalty", "franchise", "امتياز", "munch fee")),
        ("marketing", ("marketing", "advert", "تسويق", "دعاية")),
        ("utilities", ("electric", "water", "telecom", "utility", "كهرب", "مياه", "اتصالات")),
        ("government", ("government", "visa", "iqama", "municip", "حكوم", "إقامة", "بلدي")),
        ("insurance", ("insurance", "تأمين")),
        ("bank_fees", ("bank fee", "merchant", "mada", "رسوم بن")),
        ("depreciation", ("depreci", "إهلاك")),
    ]
    for bucket, tokens in groups:
        if any(token in text for token in tokens):
            return bucket
    return "other"


for line in lines:
    aid = line["account_id"][0] if isinstance(line.get("account_id"), list) else line.get("account_id")
    account = account_map.get(aid, {})
    account_type = account.get("account_type")
    balance = float(line.get("balance") or 0.0)
    m = monthly[month_key(line["date"])]
    if account_type in {"income", "income_other"}:
        m["revenue"] += -balance
    elif account_type == "expense_direct_cost":
        m["cogs"] += balance
    else:
        m["opex"] += balance
        m["expenses"][expense_bucket(account)] += balance

month_rows = []
for key in sorted(monthly):
    row = monthly[key]
    gp = row["revenue"] - row["cogs"]
    np = gp - row["opex"]
    month_rows.append({
        "month": key,
        "revenue": round(row["revenue"], 2),
        "cogs": round(row["cogs"], 2),
        "gross_profit": round(gp, 2),
        "gross_margin": round(gp / row["revenue"] * 100, 2) if row["revenue"] else 0,
        "opex": round(row["opex"], 2),
        "net_profit": round(np, 2),
        "net_margin": round(np / row["revenue"] * 100, 2) if row["revenue"] else 0,
        "expenses": {k: round(v, 2) for k, v in row["expenses"].items()},
    })


def total_rows(rows):
    out = {k: round(sum(float(r.get(k) or 0) for r in rows), 2)
           for k in ("revenue", "cogs", "gross_profit", "opex", "net_profit")}
    out["gross_margin"] = round(out["gross_profit"] / out["revenue"] * 100, 2) if out["revenue"] else 0
    out["net_margin"] = round(out["net_profit"] / out["revenue"] * 100, 2) if out["revenue"] else 0
    expenses = defaultdict(float)
    for row in rows:
        for key, value in (row.get("expenses") or {}).items():
            expenses[key] += float(value or 0)
    out["expenses"] = {k: round(v, 2) for k, v in expenses.items()}
    return out


annual = []
for year in sorted({r["month"][:4] for r in month_rows}):
    values = [r for r in month_rows if r["month"].startswith(year)]
    annual.append({"year": year, **total_rows(values)})

current_year = str(period_end.year)
closed_month_count = period_end.month
current_rows = [r for r in month_rows if r["month"].startswith(current_year)]
prior_prefix = str(period_end.year - 1)
prior_rows = [r for r in month_rows if r["month"].startswith(prior_prefix)
              and int(r["month"][5:7]) <= closed_month_count]
current_ytd = total_rows(current_rows)
prior_ytd = total_rows(prior_rows)

# Historical POS sales by branch. These are operational sales and are kept
# separate from the statutory GL revenue above.
configs = paged("pos.config", [], ["id", "name", "active"])
config_names = {c["id"]: c["name"] for c in configs}
branch_months = defaultdict(lambda: defaultdict(lambda: {"revenue": 0.0, "transactions": 0}))
order_groups = call("pos.order", "read_group", [[
    ["state", "in", ["done", "invoiced"]],
    ["date_order", "<=", period_end_s + " 23:59:59"],
], ["amount_total:sum"], ["config_id", "date_order:month"]], {"lazy": False})
for group in order_groups:
    cfg = group.get("config_id")
    cid = cfg[0] if isinstance(cfg, list) else cfg
    name = (cfg[1] if isinstance(cfg, list) and len(cfg) > 1 else config_names.get(cid, str(cid)))
    date_floor = next((term[2] for term in group.get("__domain", [])
                       if isinstance(term, list) and len(term) >= 3
                       and term[0] == "date_order" and term[1] == ">="), None)
    if not date_floor:
        raise SystemExit("Odoo did not return a monthly boundary for POS aggregation")
    mk = month_key(date_floor)
    branch_months[name][mk]["revenue"] += float(group.get("amount_total") or 0)
    branch_months[name][mk]["transactions"] += int(group.get("__count") or 0)

palette = ["#2ba9ed", "#e92c30", "#22c55e", "#f59e0b", "#8b5cf6", "#06b6d4", "#ec4899"]
branches = []
total_pos_ytd = sum(v["revenue"] for months in branch_months.values()
                    for key, v in months.items() if key.startswith(current_year))
for idx, (name, values) in enumerate(sorted(branch_months.items())):
    ytd_sales = sum(v["revenue"] for key, v in values.items() if key.startswith(current_year))
    share = ytd_sales / total_pos_ytd if total_pos_ytd else 0
    branches.append({
        "name": name, "color": palette[idx % len(palette)],
        "monthly": {k: {"revenue": round(v["revenue"], 2), "transactions": v["transactions"]}
                    for k, v in sorted(values.items())},
        "ytd_revenue": round(ytd_sales, 2), "share": round(share * 100, 2),
        "estimated_gross_profit": round(current_ytd["gross_profit"] * share, 2),
        "estimated_opex": round(current_ytd["opex"] * share, 2),
        "estimated_net_profit": round(current_ytd["net_profit"] * share, 2),
    })
branches.sort(key=lambda b: b["ytd_revenue"], reverse=True)

data = {
    "schema_version": 2,
    "meta": {
        "generated_at": datetime.now(RIYADH).isoformat(timespec="minutes"),
        "earliest_date": earliest, "period_end": period_end_s,
        "current_year": current_year, "closed_months": closed_month_count,
        "source": "Odoo — posted general ledger and POS",
        "basis": "Cumulative through the latest closed calendar month",
        "currency": "SAR",
    },
    "months": month_rows,
    "annual": annual,
    "current_ytd": current_ytd,
    "prior_ytd": prior_ytd,
    "branches": branches,
    "data_quality": {
        "rent_timing": "Rent is shown as posted in Odoo. Payment timing may distort a month until lease schedules are supplied.",
        "branch_profit": "Branch profit is an allocation estimate based on POS sales share; company P&L is based on posted GL entries.",
    },
}
with open("data.json", "w", encoding="utf-8") as handle:
    json.dump(data, handle, ensure_ascii=False, indent=2)
print(f"Built {len(month_rows)} months from {earliest} through {period_end_s}; {len(branches)} POS branches")
