import datetime

# --- Basic Tools ---
def calculator(a: float, b: float, operation: str = "add") -> float:
    """
    Performs basic arithmetic operations.
    Args:
        a: First number.
        b: Second number.
        operation: 'add', 'subtract', 'multiply', 'divide'.
    """
    print(f"[TOOL] 🧮 Calculator: {a} {operation} {b}")
    if operation == "add": return a + b
    elif operation == "subtract": return a - b
    elif operation == "multiply": return a * b
    elif operation == "divide": 
        return a / b if b != 0 else 0
    return 0

def get_system_time() -> str:
    """Returns the current system time and date."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[TOOL] ⌚ Time Check: {now}")
    return now

def search_database(query: str) -> str:
    """
    Mock Search Tool for internal database.
    Args:
        query: The search term.
    """
    print(f"[TOOL] 🔍 Searching DB for: {query}")
    # Mock Results
    if "diva" in query.lower():
        return "Divaparadises is a cutting-edge AI platform for Creators."
    elif "gemini" in query.lower():
        return "Gemini is a multimodal AI model from Google."
    return "No records found."

# --- Smart Home Tools (Advanced FC) ---
def set_light_values(brightness: int, color_temp: str) -> dict:
    """
    Set the brightness and color temperature of a room light.
    Args:
        brightness: Light level from 0 to 100. Zero is off.
        color_temp: 'daylight', 'cool', or 'warm'.
    """
    print(f"[TOOL] 💡 Lights: {brightness}% | Color: {color_temp}")
    return {"brightness": brightness, "colorTemperature": color_temp}

def power_disco_ball(power: bool) -> dict:
    """
    Powers the spinning disco ball.
    Args:
        power: True to turn on, False to turn off.
    """
    state = "ON" if power else "OFF"
    print(f"[TOOL] 🪩 Disco Ball: {state}")
    return {"status": f"Disco ball powered {state}"}

def start_music(energetic: bool, loud: bool) -> dict:
    """
    Play music matching parameters.
    Args:
        energetic: True for high energy music.
        loud: True for high volume.
    """
    genre = "Techno" if energetic else "Lo-Fi"
    vol = "MAX" if loud else "Medium"
    print(f"[TOOL] 🎵 Music: {genre} at {vol} Volume")
    return {"music_type": genre, "volume": vol}

# Tool Registry List
ALL_TOOLS = [
    calculator, 
    get_system_time, 
    search_database,
    set_light_values,
    power_disco_ball,
    start_music
]
