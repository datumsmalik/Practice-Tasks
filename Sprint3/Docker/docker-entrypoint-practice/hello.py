# hello.py
import sys  #is a list of command-line arguments.



name = sys.argv[1] if len(sys.argv) > 1 else "World"
#sys.argv[1] is the first argument after the script name.
#len(sys.argv) > 1 checks if an argument is given.
#If yes → assign it to name.
#If no → use "World".



print(f"Hello, {name}!")




# Build the Image (docker build -t entrypoint-demo .)
# Run without any args (docker run --rm entrypoint-demo) default arg jo k ham ne world rakha hua he 
# Run with argument (docker run --rm entrypoint-demo Sufyan)  sufyan ko append kr de ga hello k sath