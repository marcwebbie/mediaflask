import argparse
import runpy


parser = argparse.ArgumentParser()
parser.add_argument("interface", choices=["web", "gtk"], help="User interface")
args = parser.parse_args()

if args.interface == "web":
    runpy.run_module("mediaflask.application")
    # from . import app
    # app.main()
