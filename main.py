import argparse
from dotenv import load_dotenv
import sys
from osint import username_analyzer, email_analyzer, domain_analyzer, report_generator
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


def analyze_by_params(args):
    try:
        if args.username:
            target = validate_target("Usuario", args.username)
            results = username_analyzer.analyze(target)
            report_generator.show_results_username(results, target)
        elif args.email:
            target = validate_target("Email", args.email)
            results = email_analyzer.analyze(target)
            report_generator.show_results_email(results, target)
        elif args.domain:
            target = validate_target("Dominio", args.domain)
            results = domain_analyzer.analyze(target)
            report_generator.show_results_domain(results, target)
    except ValueError as error:
        print(f"❌ {error}")
        raise SystemExit(2)
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
    analysis_args = parser.add_mutually_exclusive_group()
    analysis_args.add_argument(
        "-u", "--username", help="Username to analyze on social networks"
    )
    analysis_args.add_argument(
        "-e", "--email", help="Email address to search for breaches"
    )
    analysis_args.add_argument(
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
                username = validate_target("Usuario", input("🔎 Enter the username to analyze: "))
                try:
                    results = username_analyzer.analyze(username)
                    report_generator.show_results_username(results, username)
                    username_analyzer.print_username_results(results)

                except Exception as e:
                    print(f"⚠️  Error analyzing username: {e}")
            elif choice == "2":
                # Email leak analysis
                email = validate_target("Email", input("📧 Enter the email address to search: "))
                try:
                    results = email_analyzer.analyze(email)
                    report_generator.show_results_email(results, email)
                    # email_analyzer.print_email_results(results)
                except Exception as e:
                    print(f"⚠️  Error analyzing email: {e}")
            elif choice == "3":
                # Domain/company public info analysis
                domain = validate_target("Dominio", input("🌐 Enter the domain or company: "))
                try:
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
