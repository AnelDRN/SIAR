from django.core.management.base import BaseCommand
from analysis.models import Species

class Command(BaseCommand):
    help = 'Generates sample species data.'

    def handle(self, *args, **options):
        self.stdout.write("Generating sample species data...")

        species_data = [
            {"name": "Roble", "scientific_name": "Quercus robur", "description": "Árbol de hoja caduca, nativo de Europa."},
            {"name": "Haya", "scientific_name": "Fagus sylvatica", "description": "Árbol de hoja caduca, común en bosques templados."},
            {"name": "Pino Silvestre", "scientific_name": "Pinus sylvestris", "description": "Conífera de hoja perenne, adaptable a diversos climas."}, 
            {"name": "Abeto", "scientific_name": "Abies alba", "description": "Conífera de gran tamaño, prefiere climas fríos y húmedos."}, 
            {"name": "Arce", "scientific_name": "Acer platanoides", "description": "Árbol ornamental, conocido por sus hojas lobuladas."}, 
        ]

        for data in species_data:
            species, created = Species.objects.get_or_create(
                scientific_name=data["scientific_name"],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created species: {species.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Species already exists: {species.name}'))

        self.stdout.write(self.style.SUCCESS("Sample species data generation complete."))
