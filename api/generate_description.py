import nltk.data
from nltk import word_tokenize


class WeatherDescriptionGenerator:
    def __init__(self):
        # list of locations, weather conditions, times
        self.provinces = ["central", "eastern", "north-central", "northern", "north-western", "sabaragamuwa",
                     "southern", "uva", "western"]
        self.districts = ["ampara", "anuradhapura", "badulla", "batticaloa", "colombo", "galle", "gampaha", "hambantota", "jaffna",
                     "kalutara", "kandy", "kegalle", "kilinochchi", "kurunegala", "mannar", "matale", "matara",
                     "moneragala", "mullaitivu", "nuwara eliya", "nuwara-eliya", "polonnaruwa",
                     "puttalam", "ratnapura", "trincomalee", "vavuniya"]
        self.weather_conditions = ["shower", "flood", "cyclone", "misty", "mist", "cloudy", "cloud", "sunny", "thunder",
                              "thunderstorm", "wind", "windy", "rainy", "rain", "foggy", "fog", "thundershower", "rough"]
        self.times = ["morning", "afternoon", "evening", "night"]

        self.related_location = {
            ("eastern", "east"): "eastern",
            ("northern", "north"): "northern",
            ("south", "southern"): "southern",
            ("western", "west"): "western"
        }

        self.related_conditions = {
            ("foggy", "misty", "fog", "mist"): "misty",
            ("rain", "rainy", "shower", "rains"): "rainy",
            ("winds", "wind"): "windy",
            ("cloud" ):"cloudy",
            ("thundershower", "thunder", "thunderstorm", "thundershowers"): "thundershower",
            ("flood"): "flood",
            ("sunny"): "sunny",
            ("cyclone"): "cyclone",
            ("rough"): "rough",
        }

        self.your_location_descriptions = {
            "eastern": "The eastern coastal belt of Sri Lanka, known for its beautiful beaches and national parks.",
            "western": "The most populous province in Sri Lanka, encompassing the capital city Colombo and coastal areas.",
            "sabaragamuwa Province": "A province in central Sri Lanka, known for its lush greenery, waterfalls, and historical sites.",
            "central": "A mountainous region in central Sri Lanka, famous for its scenic landscapes and tea plantations.",
            "north-central": "ancient cities, and historical sites, dry zone.",
            "northern": "known for its rich history and cultural heritage of tamil kovil, dry zone.",
            "north-western": "A province in northwestern Sri Lanka, known for its beaches, lagoons, and historical sites.",
            "southern": "A coastal province in southern Sri Lanka, known for its beaches, wildlife sanctuaries, and historical sites.",
            "uva": "A mountainous region in central Sri Lanka, famous for its scenic landscapes and tea plantations.",
            "polonnaruwa": "An ancient city in Sri Lanka, once a powerful kingdom with well-preserved ruins and historical sites.",
            "matale": "A city in central Sri Lanka, known for its spice gardens and scenic mountains.",
            "nuwara eliya": "A hill station in central Sri Lanka, popular for its cool climate, colonial architecture, and breathtaking views.",
            "galle": "A city on the southwestern coast of Sri Lanka, known for its beautiful Galle Dutch Fort, beaches.",
            "matara": "A coastal city in southern Sri Lanka, famous for its beaches, surfing spots.",
            "anuradhapura": "An ancient city with sthupa in Sri Lanka, once a powerful kingdom with well-preserved ruins and historical sites.",
            "colonbo": "The commercial capital of Sri Lanka, known for its skyscrapers, shopping malls, and colonial architecture."
        }

        self.your_weather_descriptions = {
            "rainy": "rain+++ falling, rain drops, wet environment, single figure walking with an umbrella.",
            "shower": "rain+++ falling, rain drops, wet environment, single figure walking with an umbrella",
            "thundershower": "A thunderstorm with rain+++ falling, lightning, continuous thundering.",
            "windy": "strong winds++ blowing.",
            "foggy": "a thin layer of fog or mist obscuring the view, creating a somewhat ethereal atmosphere.",
            "flood": "A large amount of water overflowing from a river or lake, causing inundation and potential damage.",
            "sunny": "Having clear skies and bright sunshine, providing warmth and light.",
            "cyclone": "A severe storm with a low-pressure center and strong, swirling winds that can cause significant damage.",
            "rough": "Having a turbulent or choppy surface, especially referring to the sea or ocean.",
        }

        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def _extract_info(self, sentence):
        print(sentence)
        locations = []
        weather_events = []
        for word in sentence:
            if word in self.provinces:
                locations.append(word)
                print(word)
            else:
                for key, value in self.related_location.items():
                    if word in key:
                        locations.append(value)
                        print(value)
                        break
            if word in self.districts:
                locations.append(word)
                print(word)
            if word in self.weather_conditions:
                weather_events.append(word)
                print(word)
            else:
                for key, value in self.related_conditions.items():
                    if word in key:
                        weather_events.append(value)
                        print(value)
                        break


        refined_weather_events = []
        for weather in weather_events:
            found = False
            for key, value in self.related_conditions.items():
                if weather in key:
                    refined_weather_events.append(value)
                    found = True
                    break
            if not found:
                refined_weather_events.append(weather)

        standard_locations=[]
        for location in locations:
            found = False
            for key, value in self.related_location.items():
                if location in key:
                    standard_locations.append(value)
                    found = True
                    break
            if not found:
                standard_locations.append(location)

        return standard_locations, refined_weather_events

    def generate_descriptions(self, sentence):
        sentences = self.tokenizer.tokenize(sentence)
        descriptions_set = set()

        for sentence in sentences:
            if "nuwara eliya" in sentence.lower():
                sentence = sentence.replace("Nuwara Eliya", "nuwara-eliya")
            word_list = word_tokenize(sentence.lower())
            locations, weather_events = self._extract_info(word_list)
            for weather_event in weather_events:
                for location in locations:
                    description = f"There will be {weather_event}++ means "
                    if weather_event in self.your_weather_descriptions:
                        description += self.your_weather_descriptions[weather_event]
                    description += f" In {location}+, place in Sri Lanka "
                    if location in self.your_location_descriptions:
                        description += self.your_location_descriptions[location] + " "
                    description += ("realistic++, detailed, intricate, focused, extreme details, HD photography, masterpiece")
                    descriptions_set.add((description.strip(), location, weather_event))

        return list(descriptions_set)