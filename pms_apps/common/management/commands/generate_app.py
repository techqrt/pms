import os
import shutil
import re
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Generate a new Django app in a predefined location using a custom template."

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help="Name of the new Django app")

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        camel_case_name = ''.join(word.capitalize() for word in app_name.split('_'))  # Convert to CamelCase

        # Define paths
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))  # Go up to `erp_backend`
        template_path = os.path.join(project_root, "remedizz", "app_template")  # Your app template
        destination_path = os.path.join(project_root, "remedizz_apps", app_name)  # Where new apps will be created

        # Check if the app already exists
        if os.path.exists(destination_path):
            raise CommandError(f"App '{app_name}' already exists at {destination_path}!")

        # Run django-admin startapp with the template
        os.system(f"django-admin startapp {app_name} --template={template_path}")

        # Move the generated app to the predefined location
        shutil.move(app_name, destination_path)

        # Replace `app_template` and `AppTemplate` in all files
        self.replace_placeholders(destination_path, app_name, camel_case_name)

        self.stdout.write(self.style.SUCCESS(f"Successfully created app '{app_name}' in {destination_path}"))

    def replace_placeholders(self, destination_path, app_name, camel_case_name):
        """
        Replaces 'app_template' with app_name and 'AppTemplate' with camel_case_name in all files.
        """
        for root, _, files in os.walk(destination_path):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace `app_template` with `app_name` (same format)
                content = re.sub(r'app_template', app_name, content)

                # Replace `AppTemplate` with `camel_case_name`
                content = re.sub(r'AppTemplate', camel_case_name, content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
