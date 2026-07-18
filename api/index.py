import os

# Vercel Python runtime entrypoint for Django
if os.getenv("VERCEL") == "1":
	os.environ["DEBUG"] = "False"

	allowed_hosts = [
		host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()
	]
	for required_host in ["localhost", "127.0.0.1", ".vercel.app"]:
		if required_host not in allowed_hosts:
			allowed_hosts.append(required_host)

	vercel_url = os.getenv("VERCEL_URL", "").strip()
	if vercel_url and vercel_url not in allowed_hosts:
		allowed_hosts.append(vercel_url)

	os.environ["ALLOWED_HOSTS"] = ",".join(allowed_hosts)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402
