from pathlib import Path
import re
import sys

build_dir = Path(sys.argv[1])
revision = sys.argv[2]

index_path = build_dir / "index.html"
bootstrap_path = build_dir / "flutter_bootstrap.js"

index = index_path.read_text(encoding="utf-8")

cache_guard = f"""
<script>
(async function () {{
  const buildId = "{revision}";
  const key = "eman_web_build_id";
  const previous = localStorage.getItem(key);

  if (previous !== buildId) {{
    if ("serviceWorker" in navigator) {{
      const registrations = await navigator.serviceWorker.getRegistrations();
      await Promise.all(registrations.map((registration) => registration.unregister()));
    }}

    if ("caches" in window) {{
      const cacheNames = await caches.keys();
      await Promise.all(cacheNames.map((name) => caches.delete(name)));
    }}

    localStorage.setItem(key, buildId);

    if (!location.search.includes("build=" + buildId)) {{
      const url = new URL(location.href);
      url.searchParams.set("build", buildId);
      location.replace(url.toString());
      return;
    }}
  }}
}})();
</script>
"""

if "</head>" in index:
    index = index.replace("</head>", cache_guard + "\n</head>", 1)

index_path.write_text(index, encoding="utf-8")

# Flet/Flutter service worker остаётся доступным для PWA, но после каждой
# новой публикации старый worker и его Cache Storage принудительно удаляются.
