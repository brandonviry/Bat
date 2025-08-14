#!/usr/bin/env python3
"""
Battery Monitor - Point d'entrée principal
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import BatteryConfig
from src.monitor import BatteryMonitorApp


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Battery Monitor - Surveillance professionnelle de batterie",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                           # Utilise la configuration par défaut
  python main.py --low-threshold 15        # Seuil batterie faible à 15%
  python main.py --full-threshold 85       # Seuil batterie pleine à 85%
  python main.py --interval 30             # Vérification toutes les 30 secondes
  python main.py --no-notifications        # Désactive les notifications
  python main.py --log-level DEBUG         # Active les logs détaillés
  python main.py --log-file battery.log    # Sauvegarde les logs dans un fichier

Variables d'environnement supportées:
  BAT_LOW_THRESHOLD      Seuil batterie faible (défaut: 20)
  BAT_FULL_THRESHOLD     Seuil batterie pleine (défaut: 80)
  BAT_CHECK_INTERVAL     Intervalle de vérification en secondes (défaut: 60)
  BAT_APP_NAME           Nom de l'application (défaut: Battery Monitor)
  BAT_ENABLE_NOTIFICATIONS  Active/désactive les notifications (défaut: true)
  BAT_LOG_LEVEL          Niveau de log (défaut: INFO)
  BAT_LOG_FILE           Fichier de log (optionnel)
        """
    )
    
    parser.add_argument(
        "--low-threshold",
        type=int,
        metavar="PERCENT",
        help="Seuil de batterie faible en pourcentage (défaut: 20)"
    )
    
    parser.add_argument(
        "--full-threshold",
        type=int,
        metavar="PERCENT",
        help="Seuil de batterie pleine en pourcentage (défaut: 80)"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        metavar="SECONDS",
        help="Intervalle de vérification en secondes (défaut: 60)"
    )
    
    parser.add_argument(
        "--app-name",
        type=str,
        metavar="NAME",
        help="Nom de l'application pour les notifications (défaut: Battery Monitor)"
    )
    
    parser.add_argument(
        "--no-notifications",
        action="store_true",
        help="Désactive les notifications système"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Niveau de logging (défaut: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        metavar="FILE",
        help="Fichier de log (optionnel)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Battery Monitor 1.0.0"
    )
    
    return parser


def create_config_from_args(args: argparse.Namespace) -> BatteryConfig:
    """Create configuration from command line arguments"""
    # Start with environment-based config
    config = BatteryConfig.from_env()
    
    # Override with command line arguments if provided
    if args.low_threshold is not None:
        config.low_battery_threshold = args.low_threshold
    
    if args.full_threshold is not None:
        config.full_battery_threshold = args.full_threshold
    
    if args.interval is not None:
        config.check_interval = args.interval
    
    if args.app_name is not None:
        config.app_name = args.app_name
    
    if args.no_notifications:
        config.enable_notifications = False
    
    if args.log_level is not None:
        config.log_level = args.log_level
    
    if args.log_file is not None:
        config.log_file = args.log_file
    
    return config


def main() -> int:
    """Main entry point"""
    try:
        # Parse command line arguments
        parser = create_parser()
        args = parser.parse_args()
        
        # Create configuration
        config = create_config_from_args(args)
        
        # Validate configuration
        config.validate()
        
        # Create and run the application
        app = BatteryMonitorApp(config)
        app.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
        return 0
    
    except ValueError as e:
        print(f"Erreur de configuration: {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"Erreur inattendue: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
