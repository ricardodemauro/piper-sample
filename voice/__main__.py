import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Piper TTS executor - switch between different synthesis modes"
    )
    parser.add_argument(
        "--executor",
        choices=["main", "stream", "stream_memory", "stream_cli"],
        default="main",
        help="Choose which executor to run (default: main)"
    )
    
    args = parser.parse_args()
    
    if args.executor == "main":
        from . import main as main_module
        main_module.run()
    elif args.executor == "stream":
        from . import stream
        stream.run()
    elif args.executor == "stream_memory":
        from . import stream_memory
        stream_memory.run()
    elif args.executor == "stream_cli":
        from . import stream_cli
        stream_cli.run()

if __name__ == "__main__":
    main()