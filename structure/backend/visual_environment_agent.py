from phue import Bridge
import matplotlib.pyplot as plt

class VisualLightAgent:
    def __init__(self, bridge_ip):
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

    def adjust_lighting(self, emotional_state):
        """
        Adjust lighting based on emotional state.
        """
        state_to_color = {
            "calm": [0.4, 0.5],  # Calming blue
            "uplifting": [0.5, 0.4],  # Uplifting yellow
            "neutral": [0.33, 0.33]  # Neutral white
        }
        color = state_to_color.get(emotional_state, [0.33, 0.33])
        for light in self.bridge.lights:
            light.xy = color

    def generate_visual(self, emotional_state):
        """
        Display visual content based on emotional state.
        """
        visuals = {
            "calm": "calm_landscape.jpg",
            "uplifting": "sunrise.jpg",
            "neutral": "neutral_background.jpg"
        }
        image_path = visuals.get(emotional_state, "neutral_background.jpg")
        try:
            img = plt.imread(image_path)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Error displaying visual: {e}")
