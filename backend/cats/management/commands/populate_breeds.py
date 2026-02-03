import os
from django.core.management.base import BaseCommand
from cats.models import CatBreed

from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the database with 67 cat breeds and their details'

    def handle(self, *args, **kwargs):
        import json
        
        # Paths
        labels_path = settings.BASE_DIR.parent / 'models' / 'breed_labels_new_run.txt'
        json_path = settings.BASE_DIR / 'cats' / 'management' / 'commands' / 'breeds_data.json'
        
        if not os.path.exists(labels_path):
             self.stdout.write(self.style.ERROR(f'Labels file not found at {labels_path}'))
             return

        # Load Breeds List
        with open(labels_path, 'r') as f:
            target_breeds = [line.strip() for line in f.readlines() if line.strip()]

        # Load API Data
        with open(json_path, 'r') as f:
            api_data = json.load(f)
        
        # Map API data by name lowercased
        api_map = {item['name'].lower(): item for item in api_data}

        # Manual overrides and fallback data for patterns/mixed breeds
        manual_data = {
            "calico": {
                "origin": "Worldwide",
                "description": "Calico is not a breed but a color pattern found in many breeds. They are almost exclusively female and known for their sassy 'tortitude'.",
                "temperament": "Sassy, Independent, Loving, Unique",
                "life_span": "12 - 16",
                "energy_level": 3,
                "health_issues": 1
            },
            "tortoiseshell": {
                "origin": "Worldwide",
                "description": "Tortoiseshell cats combine two colors other than white, usually black and orange. Like Calicos, they are famously feisty and full of personality.",
                "temperament": "Feisty, Vocal, Possessive, Affectionate",
                "life_span": "12 - 16",
                "energy_level": 4,
                "health_issues": 1
            },
            "tabby": {
                "origin": "Worldwide",
                "description": "Tabby is the most common coat pattern in domestic cats, featuring distinctive stripes, dots, or swirling patterns and a 'M' mark on the forehead.",
                "temperament": "Friendly, Outgoing, Relaxed, Variable",
                "life_span": "12 - 18",
                "energy_level": 3,
                "health_issues": 1
            },
            "tuxedo": {
                "origin": "Worldwide",
                "description": "Tuxedo cats are bicolor cats with black and white markings resembling a formal tuxedo. They are often described as significantly more intelligent and affectionate.",
                "temperament": "Intelligent, Affectionate, Dog-like, Vocal",
                "life_span": "12 - 16",
                "energy_level": 4,
                "health_issues": 1
            },
            "domestic short hair": {
                "origin": "Worldwide",
                "description": "The Domestic Short Hair is a cat of mixed ancestry that does not belong to a particular recognized cat breed. They come in all shapes, sizes, and colors.",
                "temperament": "Adaptable, Friendly, Low-maintenance, Hardy",
                "life_span": "12 - 18",
                "energy_level": 3,
                "health_issues": 1
            },
             "domestic medium hair": {
                "origin": "Worldwide",
                "description": "Domestic Medium Hair cats have a coat length between short and long. They are mixed breed cats known for their diversity and hardiness.",
                "temperament": "Adaptable, Playful, Relaxed",
                "life_span": "12 - 18",
                "energy_level": 3,
                "health_issues": 1
            },
             "domestic long hair": {
                "origin": "Worldwide",
                "description": "Domestic Long Hair cats are mixed breed cats with long, luxurious fur. They require regular grooming but make beautiful, fluffy companions.",
                "temperament": "Gentle, Laid-back, Affectionate",
                "life_span": "12 - 18",
                "energy_level": 2,
                "health_issues": 1
            },
            "extra-toes cat - hemingway polydactyl": {
                "origin": "United States (Key West)",
                "description": "Polydactyl cats are born with more than the usual number of toes on one or more of their paws. Famous for living at the Ernest Hemingway Home.",
                "temperament": "Clumsy, Affectionate, Unique, Lucky",
                "life_span": "12 - 15",
                "energy_level": 3,
                "health_issues": 1
            },
            "tiger": {
                "origin": "Worldwide",
                "description": "Refers to a specific mackerel tabby pattern that resembles a tiger's stripes. These cats are often affectionate domestic shorthairs.",
                "temperament": "Bold, Playful, Hunter-like",
                "life_span": "12 - 16",
                "energy_level": 4,
                "health_issues": 1
            }
        }

        # Alias Mapping (Label -> Key in api_map or manual_data)
        aliases = {
            "applehead siamese": "siamese",
            "canadian hairless": "sphynx",
            "chinchilla": "persian",
            "dilute calico": "calico",
            "dilute tortoiseshell": "tortoiseshell",
            "havana": "havana brown",
            "oriental long hair": "oriental",
            "oriental short hair": "oriental",
            "oriental tabby": "oriental",
            "silver": "tabby", # Treat silver as a tabby variant for data purposes
            "torbie": "tortoiseshell", # Tortie-Tabby mix
        }

        created_count = 0
        updated_count = 0
        
        for breed_name in target_breeds:
            key = breed_name.lower()
            
            # Resolve alias if exists
            if key in aliases:
                key = aliases[key]
            
            # Try finding in API data first
            match_data = api_map.get(key)
            
            # If not in API, check manual data (for patterns/mixed)
            if not match_data:
                match_data = manual_data.get(key)
            
            # If still not found, try robust fuzzy matching
            if not match_data:
                 for k, v in api_map.items():
                    if k in key or key in k:
                        match_data = v
                        break

            # Construct fields
            if match_data:
                origin = match_data.get('origin', 'Unknown')
                desc = match_data.get('description', f"The {breed_name} is a beautiful cat.")
                habits = match_data.get('temperament', 'Friendly and active.')
                life_span = match_data.get('life_span', '12-15')
                health_level = match_data.get('health_issues', 2)
                
                health = f"Average Life Span: {life_span} years. General Health Robustness: {5-health_level}/5."
                
                energy = match_data.get('energy_level', 3)
                if energy >= 4:
                    food = "High-protein diet recommended to support high energy levels. Needs plenty of hydration."
                elif energy <= 2:
                    food = "Calorie-controlled diet recommended to prevent obesity. Avoid free-feeding."
                else:
                    food = "Balanced dry and wet food diet. Adjust portions based on activity."
            else:
                # Absolute fallback
                origin = "Unknown"
                desc = f"The {breed_name} is a unique breed recognized by our classifier."
                habits = "Unique personality traits."
                health = "Regular vet checkups recommended."
                food = "Standard balanced nutrition."
                self.stdout.write(self.style.WARNING(f"Using fallback for: {breed_name}"))

            obj, created = CatBreed.objects.update_or_create(
                name=breed_name,
                defaults={
                    "origin": origin,
                    "description": desc,
                    "health_info": health,
                    "habits": habits,
                    "food_recommendations": food
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Done! Created: {created_count}, Updated: {updated_count}'))
