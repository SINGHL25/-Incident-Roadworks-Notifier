# -Incident-Roadworks-Notifier
🚗 Incident &amp; Roadworks Notifier — Push notifications for accidents, diversions, or planned maintenance.
Core Features
Load real-time feeds (QLD, VIC, NSW — Australia).

Fallback to sample JSON if API not accessible (for offline/GitHub demo).

Filter by:

Date/time

Event type (accident, roadwork, closure, weather hazard)

Severity

Live map with markers + popups.

Event table with export to CSV.

Push alert stubs (can connect later to Pushover/Twilio).

Tech Stack
Streamlit (dashboard)

Pandas (data processing)

Folium (map rendering)

Requests (API fetch)

python-dotenv (manage API keys)

Geopandas (optional: for shape filtering)

