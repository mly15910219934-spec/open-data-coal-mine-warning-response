from .download_data import main as download
from .validate_data import main as validate
from .summarize_case_screening import main as cases
from .v2_pipeline import run_all_v2


def main():
    download(); validate(); run_all_v2(); cases()


if __name__ == "__main__": main()
