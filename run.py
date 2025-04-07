from cli.src.start import start as start_cli
import subprocess
import atexit

def main() -> None:

    # Start the SQLite server in a separate process with logging
    with open("db_handler.log", "w") as log_file:
        # Run the script as a subprocess
        subprocess.Popen(
            ["python3", "db/src/start.py"],  
            stdout=log_file,                
            stderr=subprocess.STDOUT
        )
    
    atexit.register(
        lambda: subprocess.call(["pkill", "-f", "db/src/start.py"])
    )


    start_cli()


if __name__ == "__main__":
    main()