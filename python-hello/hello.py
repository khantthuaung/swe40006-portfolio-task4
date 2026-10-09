import platform
from datetime import datetime, timezone

print("Hello from my Python Docker app!")
print("Unit: SWE40006 Software Deployment and Evolution")
print(f"Python runtime: {platform.python_version()}")
print(f"Execution time: {datetime.now(timezone.utc).isoformat()}")