import nltk.data
from nltk import word_tokenize
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag

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
            ("rain", "rainy", "shower", "rains", "showers"): "rainy",
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
            "northern": "known for its rich history and cultural heritage of tamil kovil, palm trees, dry zone.",
            "north-western": "A province in northwestern Sri Lanka, known for its beaches, lagoons, and historical sites.",
            "southern": "A coastal province in southern Sri Lanka, known for its beaches, wildlife sanctuaries, and historical sites.",
            "uva": "A mountainous region in central Sri Lanka, famous for its scenic landscapes and tea plantations.",
            "Polonnaruwa": "An ancient city in Sri Lanka, once a powerful kingdom with well-preserved ruins and historical sites. Notable attractions include the Royal Palace, the Gal Vihara rock temple, and the Parakrama Samudra, an impressive man-made reservoir.",
            "Jaffna": "Known for its rich history and cultural heritage of Tamil kovil, palm trees, and dry zone. Key sites include the Nallur Kandaswamy Kovil, the Jaffna Fort, and the scenic Casuarina Beach. Jaffna is also famous for its vibrant local cuisine and traditional festivals.",
            "Matale": "A city in central Sri Lanka, known for its spice gardens and scenic mountains. Attractions include the Aluvihare Rock Temple, Sembuwatta Lake, and the Knuckles Mountain Range, offering stunning hiking trails and panoramic views.",
            "Nuwara Eliya": "A hill station in central Sri Lanka, popular for its cool climate, colonial architecture, and breathtaking views. Highlights include the picturesque Gregory Lake, the Hakgala Botanical Garden, and lush tea plantations where visitors can learn about tea production.",
            "Galle": "A city on the southwestern coast of Sri Lanka, known for its beautiful Galle Dutch Fort, beaches, and colonial architecture. The fort area is filled with charming boutiques, cafes, and museums. Unawatuna Beach and Jungle Beach are popular nearby spots for relaxation and water activities.",
            "Matara": "A coastal city in southern Sri Lanka, famous for its beaches, surfing spots, and historical landmarks. Key attractions include the Star Fort, Polhena Beach, and the Dondra Head Lighthouse, the southernmost point of Sri Lanka.",
            "Anuradhapura": "An ancient city with stupas in Sri Lanka, once a powerful kingdom with well-preserved ruins and historical sites. Important sites include the sacred Sri Maha Bodhi tree, the Ruwanwelisaya stupa, and the Jetavanaramaya stupa.",
            "Colombo": "The commercial capital of Sri Lanka, known for its skyscrapers, shopping malls, and colonial architecture. Major attractions include the Galle Face Green promenade, the National Museum, and the bustling Pettah Market.",
            "Hambantota": "A rapidly developing district known for the Hambantota Port, diverse wildlife sanctuaries, the scenic Bundala National Park, and the ambitious Hambantota International Cricket Stadium. The district also features beautiful beaches and the Kumana National Park, a haven for birdwatchers.",
            "Gampaha": "A district blending urban and rural landscapes, renowned for its lush greenery, historical temples like the Kelaniya Raja Maha Vihara, and the scenic Negombo Lagoon. The district is also home to the Henarathgoda Botanical Garden and the bustling town of Negombo with its vibrant fish market and beach.",
            "Kalutara": "A picturesque coastal district with stunning beaches, the iconic Kalutara Bodhiya temple, lush rubber plantations, and the serene Kalu River. The Richmond Castle and Kalutara Beach are popular tourist attractions.",
            "Kandy": "A historic city nestled in the central highlands, famous for the Temple of the Sacred Tooth Relic, the scenic Kandy Lake, Peradeniya Botanical Gardens, and its rich cultural heritage. The annual Esala Perahera festival showcases traditional dances, music, and beautifully decorated elephants.",
            "Badulla": "A district in the central highlands, celebrated for its scenic tea plantations, cascading waterfalls like Dunhinda Falls, historic sites such as the Muthiyangana Raja Maha Viharaya, and picturesque train journeys through the mountains.",
            "Kurunegala": "Known for its unique rock formations resembling elephants, lush paddy fields, coconut plantations, and historical sites like the Athugala Buddha statue atop Elephant Rock. The district is also home to several ancient temples and the scenic Kurunegala Lake.",
            "Puttalam": "A district noted for its salt production, the scenic Puttalam Lagoon, pristine beaches, and the biodiversity-rich Wilpattu National Park. The Kalpitiya Peninsula is a popular destination for kite surfing and dolphin watching.",
            "Trincomalee": "Famous for its natural deep-water harbor, stunning beaches like Nilaveli and Uppuveli, the revered Koneswaram Temple, and vibrant marine life, including opportunities for whale watching and diving. The district also features the hot springs of Kanniya and the historic Fort Frederick.",
            "Batticaloa": "A coastal district renowned for its beautiful lagoons, pristine beaches, rich cultural heritage, and historic sites such as the Batticaloa Fort. The district is also known for Batticaloa Lagoon and the annual Hindu festival at the Kokkadicholai Thaanthonreeswarar Temple.",
            "Ampara": "A district with diverse wildlife, sprawling paddy fields, and the ancient Buddhist site of Deegavapiya. Ampara is also home to the scenic Gal Oya National Park, where visitors can take boat safaris to see elephants and other wildlife.",
            "Monaragala": "Known for its unspoiled natural beauty, rich wildlife, and national parks like Yala and Gal Oya, offering lush landscapes and opportunities for eco-tourism and adventure. The district also features the ancient Maligawila Buddha statue and the stunning Diyaluma Falls.",
            "Ratnapura": "The 'City of Gems,' famous for its gem mining industry, lush greenery, stunning waterfalls like Bopath Ella, and scenic trekking opportunities in the Sinharaja Forest Reserve, a UNESCO World Heritage site.",
            "Kegalle": "Known for its extensive rubber plantations, the Pinnawala Elephant Orphanage which attracts tourists from around the world, and the scenic beauty of the surrounding hills and forests. The district also features the Bible Rock and the Kitulgala rapids, popular for white-water rafting.",
            "Kilinochchi": "A district recovering from civil conflict, marked by its vast agricultural lands, historical significance, and natural attractions such as the Iranamadu Tank, a large irrigation reservoir.",
            "Mannar": "Known for its thriving fishing industry, historical sites like the Mannar Fort, and the unique Adam's Bridge, a chain of limestone shoals connecting it to India. The district also features beautiful beaches and the ancient Baobab tree.",
            "Vavuniya": "A district with a blend of agriculture and urban development, known for its historical importance, cultural diversity, and landmarks such as the Vavuniya Archaeological Museum.",
            "Mullaitivu": "Known for its serene beaches, lagoons, and natural beauty, this district also holds historical significance from the civil conflict. The district features the Mullaitivu Lagoon and several war memorials."



        }

        self.your_weather_descriptions = {
            "rain": "rain+++ falling, rain drops, wet environment, single figure walking with an umbrella.",
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
            #lematising the word

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
        #split the sentence by _ and store in a list
        words = sentence.split("_")
        print(words)
        weather_event = words[0]
        location = words[1]

        description = f"There will be {weather_event}++ means "
        if weather_event in self.your_weather_descriptions:
            description += self.your_weather_descriptions[weather_event]
        description += f" In {location}+, place in Sri Lanka "
        if location in self.your_location_descriptions:
            description += self.your_location_descriptions[location] + " "
        description += ("realistic++, detailed, intricate, focused, extreme details, HD photography, masterpiece")

        return (description, location, weather_event)

        # def generate_descriptions(self, sentence):
        # sentences = self.tokenizer.tokenize(sentence)
        # descriptions_set = set()
        #
        # for sentence in sentences:
        #     if "nuwara eliya" in sentence.lower():
        #         sentence = sentence.replace("Nuwara Eliya", "nuwara-eliya")
        #     word_list = word_tokenize(sentence.lower())
        #     locations, weather_events = self._extract_info(word_list)
        #     for weather_event in weather_events:
        #         for location in locations:
        #             description = f"There will be {weather_event}++ means "
        #             if weather_event in self.your_weather_descriptions:
        #                 description += self.your_weather_descriptions[weather_event]
        #             description += f" In {location}+, place in Sri Lanka "
        #             if location in self.your_location_descriptions:
        #                 description += self.your_location_descriptions[location] + " "
        #             description += ("realistic++, detailed, intricate, focused, extreme details, HD photography, masterpiece")
        #             descriptions_set.add((description.strip(), location, weather_event))
        #
        # return list(descriptions_set)