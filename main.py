"""Command-line entry point; the analyzers and reports remain reusable modules."""

import argparse
from dotenv import load_dotenv

from osint import domain_analyzer, email_analyzer, report_generator, username_analyzer
from osint.input_validation import validate_target


BANNER = r"""

#### ##    ## ########  #######  ##     ## ##     ## ##    ## ######## ######## ########  
 ##  ###   ## ##       ##     ## ##     ## ##     ## ###   ##    ##    ##       ##     ## 
 ##  ####  ## ##       ##     ## ##     ## ##     ## ####  ##    ##    ##       ##     ## 
 ##  ## ## ## ######   ##     ## ######### ##     ## ## ## ##    ##    ######   ########  
 ##  ##  #### ##       ##     ## ##     ## ##     ## ##  ####    ##    ##       ##   ##   
 ##  ##   ### ##       ##     ## ##     ## ##     ## ##   ###    ##    ##       ##    ##  
#### ##    ## ##        #######  ##     ##  #######  ##    ##    ##    ######## ##     ##                                                          
                                                              
                                                                OSINT Intelligence Suite
                                                                    by SweetNight19 🕵️‍♂️

"""


MENU = """
What type of analysis do you want to perform? 🤔

1️⃣  Analyze username on social networks
2️⃣  Check email breach exposure
3️⃣  Collect public information about a domain/company
4️⃣  Exit

Select an option (1-4): """


ANALYZERS = {
    "Usuario": username_analyzer.analyze,
    "Email": email_analyzer.analyze,
    "Dominio": domain_analyzer.analyze,
}
REPORTERS = {
    "Usuario": report_generator.show_results_username,
    "Email": report_generator.show_results_email,
    "Dominio": report_generator.show_results_domain,
}


def run_analysis(kind, value):
    """Validate, execute, and report through the shared CLI workflow."""
    target = validate_target(kind, value)
    results = ANALYZERS[kind](target)
    REPORTERS[kind](results, target)
    return results


def analyze_by_params(args):
    """Run the analysis requested by argparse, if one was supplied."""
    for attribute, kind in (
        ("username", "Usuario"),
        ("email", "Email"),
        ("domain", "Dominio"),
    ):
        target = getattr(args, attribute, None)
        if target:
            try:
                run_analysis(kind, target)
            except ValueError as error:
                print(f"❌ {error}")
                raise SystemExit(2) from error
            return
    print("❌ No valid parameter provided. Use -h for help.")


def _build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "InfoHunter OSINT Suite\n\n"
            "Examples:\n"
            "  python main.py -d example.com\n"
            "  python main.py -e user@example.com\n"
            "  python main.py -u johndoe\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--username", help="Username to analyze on social networks")
    group.add_argument("-e", "--email", help="Email address to search for breaches")
    group.add_argument("-d", "--domain", help="Domain or company to collect public information")
    return parser


def main():
    load_dotenv()
    args = _build_parser().parse_args()
    if args.username or args.email or args.domain:
        analyze_by_params(args)
        return

    print(BANNER)
    while True:
        try:
            choice = input(MENU).strip()
            if choice == "4":
                print("👋 See you soon!")
                return
            if choice not in {"1", "2", "3"}:
                print("❌ Invalid option. Please try again.\n")
                continue

            kind, prompt = {
                "1": ("Usuario", "🔎 Enter the username to analyze: "),
                "2": ("Email", "📧 Enter the email address to search: "),
                "3": ("Dominio", "🌐 Enter the domain or company: "),
            }[choice]
            run_analysis(kind, input(prompt))
        except ValueError as error:
            print(f"❌ {error}")
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Exiting...")
            return
        except Exception as error:
            print(f"⚠️  Analysis failed ({type(error).__name__}).")


if __name__ == "__main__":
    main()
