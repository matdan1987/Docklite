#!/usr/bin/env python3
"""
Docklite - Einfacher Docker Container Deployer
Ein benutzerfreundliches Tool zum Deployen von Docker Containern nach Vorlagen
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List
import subprocess


class DockliteManager:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)

    def list_templates(self) -> List[str]:
        """Liste alle verfügbaren Templates auf"""
        templates = []
        for file in self.templates_dir.glob("*.yaml"):
            templates.append(file.stem)
        for file in self.templates_dir.glob("*.yml"):
            if file.stem not in templates:
                templates.append(file.stem)
        return sorted(templates)

    def load_template(self, template_name: str) -> Dict[str, Any]:
        """Lade ein Template"""
        yaml_file = self.templates_dir / f"{template_name}.yaml"
        yml_file = self.templates_dir / f"{template_name}.yml"

        template_file = yaml_file if yaml_file.exists() else yml_file

        if not template_file.exists():
            raise FileNotFoundError(f"Template '{template_name}' nicht gefunden!")

        with open(template_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def check_docker(self) -> bool:
        """Prüfe ob Docker installiert und verfügbar ist"""
        try:
            subprocess.run(['docker', '--version'],
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def deploy_container(self, template_name: str, custom_vars: Dict[str, str] = None):
        """Deploye einen Container basierend auf einem Template"""
        if not self.check_docker():
            print("❌ Docker ist nicht installiert oder nicht verfügbar!")
            print("Bitte installiere Docker: https://docs.docker.com/get-docker/")
            sys.exit(1)

        print(f"📦 Lade Template '{template_name}'...")
        template = self.load_template(template_name)

        # Ersetze Variablen falls vorhanden
        if custom_vars:
            template = self._replace_variables(template, custom_vars)

        # Interaktive Eingaben für erforderliche Variablen
        if 'variables' in template:
            print("\n🔧 Konfiguration:")
            for var_name, var_info in template['variables'].items():
                if var_name not in (custom_vars or {}):
                    prompt = var_info.get('description', var_name)
                    default = var_info.get('default', '')

                    if default:
                        value = input(f"  {prompt} [{default}]: ").strip() or default
                    else:
                        value = input(f"  {prompt}: ").strip()

                    if not custom_vars:
                        custom_vars = {}
                    custom_vars[var_name] = value

            template = self._replace_variables(template, custom_vars)

        print(f"\n🚀 Deploye Container '{template.get('name', template_name)}'...")

        # Baue den Docker run Befehl
        cmd = self._build_docker_command(template)

        print(f"\n💻 Führe aus: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            print(f"\n✅ Container erfolgreich gestartet!")

            if 'info' in template:
                print(f"\nℹ️  {template['info']}")

            # Zeige Zugriffsinformationen
            if 'ports' in template:
                print("\n🌐 Zugriff:")
                for port_mapping in template['ports']:
                    if ':' in port_mapping:
                        host_port = port_mapping.split(':')[0]
                        print(f"  http://localhost:{host_port}")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Fehler beim Starten des Containers!")
            print(f"Fehler: {e}")
            sys.exit(1)

    def _replace_variables(self, template: Dict[str, Any], variables: Dict[str, str]) -> Dict[str, Any]:
        """Ersetze Variablen im Template"""
        template_str = json.dumps(template)

        for var_name, var_value in variables.items():
            template_str = template_str.replace(f"${{{var_name}}}", str(var_value))
            template_str = template_str.replace(f"${var_name}", str(var_value))

        return json.loads(template_str)

    def _build_docker_command(self, template: Dict[str, Any]) -> List[str]:
        """Baue den Docker run Befehl aus dem Template"""
        cmd = ['docker', 'run']

        # Detached mode (im Hintergrund)
        if template.get('detached', True):
            cmd.append('-d')

        # Container Name
        if 'name' in template:
            cmd.extend(['--name', template['name']])

        # Restart Policy
        if 'restart' in template:
            cmd.extend(['--restart', template['restart']])

        # Ports
        if 'ports' in template:
            for port in template['ports']:
                cmd.extend(['-p', port])

        # Volumes
        if 'volumes' in template:
            for volume in template['volumes']:
                cmd.extend(['-v', volume])

        # Environment Variables
        if 'environment' in template:
            for env_var, env_value in template['environment'].items():
                cmd.extend(['-e', f"{env_var}={env_value}"])

        # Networks
        if 'network' in template:
            cmd.extend(['--network', template['network']])

        # Zusätzliche Optionen
        if 'options' in template:
            for option in template['options']:
                cmd.append(option)

        # Image
        cmd.append(template['image'])

        # Command
        if 'command' in template:
            if isinstance(template['command'], list):
                cmd.extend(template['command'])
            else:
                cmd.append(template['command'])

        return cmd

    def show_template_info(self, template_name: str):
        """Zeige Informationen über ein Template"""
        template = self.load_template(template_name)

        print(f"\n📋 Template: {template_name}")
        print("=" * 50)

        if 'description' in template:
            print(f"\n📝 Beschreibung:\n  {template['description']}")

        print(f"\n🐳 Image: {template['image']}")

        if 'ports' in template:
            print(f"\n🔌 Ports:")
            for port in template['ports']:
                print(f"  - {port}")

        if 'volumes' in template:
            print(f"\n💾 Volumes:")
            for volume in template['volumes']:
                print(f"  - {volume}")

        if 'environment' in template:
            print(f"\n🔧 Umgebungsvariablen:")
            for key, value in template['environment'].items():
                print(f"  - {key}={value}")

        if 'variables' in template:
            print(f"\n⚙️  Konfigurierbare Variablen:")
            for var_name, var_info in template['variables'].items():
                desc = var_info.get('description', var_name)
                default = var_info.get('default', 'keine')
                print(f"  - {var_name}: {desc} (Standard: {default})")

        print()


def main():
    parser = argparse.ArgumentParser(
        description='Docklite - Einfacher Docker Container Deployer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  docklite.py list                    # Zeige alle Templates
  docklite.py info nginx              # Zeige Template-Info
  docklite.py deploy nginx            # Deploye Nginx Container
  docklite.py deploy postgres         # Deploye PostgreSQL Container
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')

    # List Command
    subparsers.add_parser('list', help='Liste alle verfügbaren Templates')

    # Info Command
    info_parser = subparsers.add_parser('info', help='Zeige Template-Informationen')
    info_parser.add_argument('template', help='Template Name')

    # Deploy Command
    deploy_parser = subparsers.add_parser('deploy', help='Deploye einen Container')
    deploy_parser.add_argument('template', help='Template Name')
    deploy_parser.add_argument('--var', '-v', action='append',
                              help='Variable setzen (z.B. -v port=8080)')

    args = parser.parse_args()

    manager = DockliteManager()

    if args.command == 'list':
        templates = manager.list_templates()
        print("\n📦 Verfügbare Templates:")
        print("=" * 50)
        for template in templates:
            try:
                info = manager.load_template(template)
                desc = info.get('description', 'Keine Beschreibung')
                print(f"  • {template:20s} - {desc}")
            except Exception:
                print(f"  • {template}")
        print()

    elif args.command == 'info':
        try:
            manager.show_template_info(args.template)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)

    elif args.command == 'deploy':
        # Parse custom variables
        custom_vars = {}
        if args.var:
            for var in args.var:
                if '=' in var:
                    key, value = var.split('=', 1)
                    custom_vars[key] = value

        try:
            manager.deploy_container(args.template, custom_vars)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
