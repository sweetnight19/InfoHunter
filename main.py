import argparse
from dotenv import load_dotenv
import os
import sys
from osint import username_analyzer, email_analyzer, domain_analyzer, report_generator

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
2️⃣  Search for leaks and passwords by email
3️⃣  Collect public information about a domain/company
4️⃣  Exit

Select an option (1-4): """


def validate_env_vars(required_vars):
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")


def analyze_by_params(args):
    if args.username:
        results = username_analyzer.analyze(args.username)
        report_generator.show_results_username(results, args.username)
    elif args.email:
        validate_env_vars(["HIBP_API_KEY", "BREACHDIRECTORY_API_KEY", "INTELX_KEY"])
        results = email_analyzer.analyze(args.email)
        report_generator.show_results_email(results, args.email)
    elif args.domain:
        validate_env_vars(["SHODAN_API_KEY", "VT_API_KEY", "HUNTER_API_KEY"])
        results = domain_analyzer.analyze(args.domain)
        report_generator.show_results_domain(results, args.domain)
    else:
        print("❌ No valid parameter provided. Use -h for help.")


def main():
    # Load environment variables from .env
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="InfoHunter OSINT Suite\n\n"
        "Examples:\n"
        "  python main.py -d ejemplo.com\n"
        "  python main.py -e usuario@correo.com\n"
        "  python main.py -u johndoe\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-u", "--username", help="Username to analyze on social networks"
    )
    parser.add_argument(
        "-e", "--email", help="Email address to search for leaks and breaches"
    )
    parser.add_argument(
        "-d", "--domain", help="Domain or company to collect public information"
    )

    args = parser.parse_args()

    # Si se pasa algún parámetro, ejecuta en modo automático
    if args.username or args.email or args.domain:
        analyze_by_params(args)
        sys.exit(0)

    print(BANNER)
    while True:
        try:
            choice = input(MENU)
            if choice == "1":
                # Username analysis
                username = input("🔎 Enter the username to analyze: ")
                try:
                    results = username_analyzer.analyze(username)
                    report_generator.show_results_username(results, username)
                    username_analyzer.print_username_results(results)

                except Exception as e:
                    print(f"⚠️  Error analyzing username: {e}")
            elif choice == "2":
                # Email leak analysis
                email = input("📧 Enter the email address to search: ")
                try:
                    validate_env_vars(["HIBP_API_KEY"])
                    validate_env_vars(["BREACHDIRECTORY_API_KEY"])
                    validate_env_vars(["INTELX_KEY"])
                    results = email_analyzer.analyze(email)
                    report_generator.show_results_email(results, email)
                    # email_analyzer.print_email_results(results)
                except Exception as e:
                    print(f"⚠️  Error analyzing email: {e}")
            elif choice == "3":
                # Domain/company public info analysis
                domain = input("🌐 Enter the domain or company: ")
                try:
                    validate_env_vars(
                        ["SHODAN_API_KEY", "VT_API_KEY", "HUNTER_API_KEY"]
                    )
                    results = domain_analyzer.analyze(domain)
                    report_generator.show_results_domain(results, domain)
                except Exception as e:
                    print(f"⚠️  Error analyzing domain: {e}")
            elif choice == "4":
                print("👋 See you soon!")
                sys.exit(0)
            else:
                print("❌ Invalid option. Please try again.\n")
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️  Unexpected error: {e}")


if __name__ == "__main__":
    main()
