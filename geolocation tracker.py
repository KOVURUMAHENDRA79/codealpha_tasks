import requests
import folium
import webbrowser
from datetime import datetime

def fetch_geolocation(api_url='http://ip-api.com/json/'):
    """Fetch geolocation data from IP-API."""
    try:
        response = requests.get(api_url, timeout=10)  # Add timeout
        response.raise_for_status()  # Raise HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None

def log_location(data, filename="location_log.txt"):
    """Save location data to a file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:  # Append mode to log multiple runs
        f.write(f"\n--- Geolocation Log ({timestamp}) ---\n")
        f.write(f"IP: {data.get('query', 'N/A')}\n")
        f.write(f"City: {data.get('city', 'N/A')}\n")
        f.write(f"Country: {data.get('country', 'N/A')}\n")
        f.write(f"ISP: {data.get('isp', 'N/A')}\n")
        f.write(f"Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n")

def create_map(data, filename="geolocation_map.html"):
    """Generate a Folium map with marker and circle."""
    lat, lon = data.get('lat'), data.get('lon')
    if not (lat and lon):
        raise ValueError("Invalid coordinates.")

    map_obj = folium.Map(location=[lat, lon], zoom_start=13)
    popup_info = f"""
        <b>{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}</b><br>
        IP: {data.get('query', 'N/A')}<br>
        ISP: {data.get('isp', 'N/A')}
    """
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_info, max_width=250),
        tooltip="Your Approximate Location",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map_obj)

    folium.Circle(
        location=[lat, lon],
        radius=500,
        color='blue',
        fill=True,
        fill_opacity=0.1
    ).add_to(map_obj)

    map_obj.save(filename)
    return filename

def main():
    data = fetch_geolocation()
    if not data or data.get('status') != 'success':
        print("Failed to fetch geolocation data.")
        return

    # Print to console
    print(f"\nGeolocation Data:")
    print(f"IP: {data.get('query')}")
    print(f"City: {data.get('city')}")
    print(f"Country: {data.get('country')}")
    print(f"ISP: {data.get('isp')}")
    print(f"Coordinates: {data.get('lat')}, {data.get('lon')}")

    # Save log and generate map
    log_location(data)
    map_file = create_map(data)
    webbrowser.open(map_file)

if __name__ == "__main__":
    main()
