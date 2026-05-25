# SkyRoute Travel Agency — Backend Setup

## What's included
- `server.py` — Flask backend (API + serves frontend)
- `public/index.html` — Customer-facing landing page with booking forms
- `public/admin.html` — Admin dashboard to view & manage all bookings
- `skyroute.db` — SQLite database (auto-created on first run)

---

## Quick Start (Local)

### 1. Install Python dependencies
```bash
pip install flask
```

### 2. Run the server
```bash
python server.py
```

### 3. Open in browser
- **Customer site:** http://localhost:5000
- **Admin dashboard:** http://localhost:5000/admin

---

## What customers can submit
| Form | Fields collected |
|------|-----------------|
| ✈ Flights | Name, email, phone, trip type, from/to, dates, passengers, cabin class |
| 🏨 Hotels | Name, email, phone, destination, check-in/out, rooms, guests, type, budget |
| 🚐 Transfers | Name, email, phone, type, pickup/dropoff, date/time, vehicle, flight # |
| 📦 Cargo | Name, email, phone, service type, origin/dest, pickup date, weight, dimensions |

Each successful submission returns a unique reference like `SR-FL-250524-0001`.

---

## Admin Dashboard Features
- Live stats: total bookings, pending, confirmed, per-service counts
- Search & filter bookings by name, email, or status
- One-click **Confirm** or **Cancel** any booking
- Auto-refreshes every 30 seconds

---

## Deploying to Production (Render.com — Free)

1. Create a free account at https://render.com
2. Push this folder to a GitHub repo
3. New Web Service → connect your repo
4. Set:
   - **Build command:** `pip install flask`
   - **Start command:** `python server.py`
5. Your site goes live at `https://your-app.onrender.com`

---

## Deploying to a VPS (DigitalOcean / AWS / any Linux server)

```bash
# Install
sudo apt install python3-pip
pip3 install flask gunicorn

# Run with gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 server:app

# Or use systemd to keep it running permanently
```

---

## Future Upgrades (optional)
- Add email notifications (use `smtplib` or SendGrid API)
- Add admin password protection
- Export bookings to Excel/CSV
- Add payment integration (Paystack / Flutterwave)
