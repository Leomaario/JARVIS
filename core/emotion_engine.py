class EmotionEngine:

    def __init__(self):
        self.state="neutral"

    def set(self,emotion):
        self.state=emotion

    def get_color(self):

        colors={
            "happy":"#00ffcc",
            "sad":"#3366ff",
            "angry":"#ff0033",
            "thinking":"#ffaa00",
            "listening":"#00ffff",
            "neutral":"#00ffff"
        }

        return colors.get(self.state,"#00ffff")