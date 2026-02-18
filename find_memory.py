import importlib
import pkgutil

def find_module_with_class(package_name, class_name):
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        return

    for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(name)
            if hasattr(module, class_name):
                print(f"✅ Found {class_name} in {name}")
                return
        except Exception:
            pass

print("Searching for ConversationBufferMemory...")
packages_to_check = ["langchain", "langchain_core", "langchain_community", "langchain_classic"]

found = False
for pkg in packages_to_check:
    print(f"Checking {pkg}...")
    try:
        module = importlib.import_module(pkg)
        if hasattr(module, "ConversationBufferMemory"):
             print(f"✅ Found at top level of {pkg}")
             found = True
             break
        # Check submodules commonly used
        try:
            mem = importlib.import_module(f"{pkg}.memory")
            if hasattr(mem, "ConversationBufferMemory"):
                print(f"✅ Found in {pkg}.memory")
                found = True
                break
        except ImportError:
            pass
    except ImportError:
        print(f"❌ {pkg} not installed")

if not found:
    print("❌ Could not find ConversationBufferMemory in common locations. Doing deep search...")
    # Deep search if needed, but might be slow.
    # checking langchain.memory explicit imports
