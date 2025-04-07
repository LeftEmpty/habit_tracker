from cli.src.start import start as start_cli
import subprocess

def main() -> None:

    subprocess.Popen(["python3", "-m", "db.src.start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    #cli
    start_cli()



if __name__ == "__main__":
    main()