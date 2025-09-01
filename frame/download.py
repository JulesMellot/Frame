from .display import display
from .plugins import get_plugin
import json
import os

# ensure built-in plugins are registered
from . import deviantart  # noqa: F401
from . import plex  # noqa: F401
from . import fixed_download  # noqa: F401

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "OnWeb")

def download(calibration_mode=False):
    """
    Télécharge et affiche une image
    
    Args:
        calibration_mode (bool): Si True, démarre le mode calibration
    
    Returns:
        bool: True si le téléchargement et l'affichage ont réussi, False sinon
    """
    print("=== Starting download function ===")
    
    # Si on est en mode calibration, créer et afficher l'image de calibration
    if calibration_mode:
        print("Calibration mode activated")
        try:
            from .calibration import test_orientation
            test_orientation()  # Crée l'image de calibration
            return display(calibration_mode=True)  # Affiche l'image de calibration
        except Exception as e:
            print(f"❌ Error during calibration: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    destination = os.path.join(WEB_DIR, "function.json")
    print(f"Looking for function file: {destination}")

    if not os.path.exists(destination):
        print("❌ function.json not found")
        return False

    with open(destination) as f:
        data = json.load(f)
    print(f"Function data loaded: {data}")
    
    if "function" not in data:
        print("❌ No function specified in function.json")
        return False
        
    function_name = data["function"]
    print(f"Selected function: {function_name}")

    plugin = get_plugin(function_name)
    if not plugin:
        print(f"❌ Plugin {function_name} not found")
        return False
    print(f"✅ Plugin found: {function_name}")
    
    print("Executing plugin...")
    try:
        plugin_result = plugin()
        print(f"Plugin execution result: {plugin_result}")
        
        if plugin_result:
            print("Plugin executed successfully, calling display()")
            try:
                display_result = display()
                print(f"Display function result: {display_result}")
                return True
            except Exception as e:
                print(f"❌ Error in display function: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("❌ Plugin execution failed or returned False")
            return False
    except Exception as e:
        print(f"❌ Error during plugin execution: {e}")
        import traceback
        traceback.print_exc()
        return False



