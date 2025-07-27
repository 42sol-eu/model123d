from os import system as X 
from rich import print 
from rich.logging import RichHandler
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

no = False
yes = True
false = False
true = True

def uses_package(name: str, dry_run=no) -> bool:
    """
    Check if a package is used in the project and install it if not.
    :param name: The name of the package to check.
    :param dry_run: If True, only check if the package is needed without installing.
    
    :return: True if the package is already installed or successfully installed, False otherwise.
    """
    if dry_run:
        return X(f'poetry show {name} --dry-run') == 0
    else:
        already_installed = X(f'poetry show {name}') == 0
        if already_installed:
            done = yes
        else:
            done = X(f'poetry add {name}') == 0
        
        return done

def other_package(name: str, git_repository: str, dry_run=no) -> bool:
    """
    Check if a package is used in the project from a git repository and install it if not.
    :param name: The name of the package to check.
    :param git_repository: The git repository URL of the package.
    :param dry_run: If True, only check if the package is needed without installing.
    
    :return: True if the package is already installed or successfully installed, False otherwise.
    """
    if dry_run:
        return X(f'poetry show {name} --dry-run') == 0
    else:
        already_installed = X(f'poetry show {name}') == 0
        if already_installed:
            done = yes
        else:
            if git_repository is None:
                raise ValueError("git_repository must be provided for other_package")
            else:
                
                # remove git+ prefix if it exists
                if git_repository.startswith("git+"):
                    git_repository = git_repository.replace("git+", "")
                    
                # ensure the repository URL starts with https:// or http://
                if not git_repository.startswith("https://"):
                    git_repository = f"https://{git_repository}"
                elif not git_repository.startswith("http://"):
                    git_repository = git_repository.replace("http://", "https://")
                                
                try:
                    response = requests.head(git_repository, allow_redirects=True, timeout=5)
                    if response.status_code >= 400:
                        raise ValueError(f"Git repository {git_repository} does not exist or is inaccessible (status code: {response.status_code})")
                except Exception as e:
                    raise ValueError(f"Failed to access git repository {git_repository}: {e}")
                
                print(f"[bold yellow]Installing {name} from {git_repository}...[/bold yellow]")
                                # ensure the repository URL starts with git+ if it doesn't already
                if not git_repository.startswith("git+"):
                    git_repository = f"git+{git_repository}"

                done = X(f'poetry add {git_repository}') == 0

        return done

def non_existing_package(name: str, git_repository: str, dry_run=no) -> bool:
    logger.debug(f"This package {name} does not exist.")
    return True

def install(no_root=yes):
    """
    Install all required packages for the project.
    """
    if no_root:
        X(f'poetry install --no-root')
    else:
        X(f'poetry install')

uses_package("rich")
uses_package("lib3mf")
uses_package("trimesh")
install()
non_existing_package('py3mf', git_repository='github.com/tamasd/py3mf.git') # ChatGPT bogusly suggested this package, but it does not exist.