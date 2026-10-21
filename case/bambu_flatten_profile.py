# Flatten a Bambu Studio system profile (inherits + include templates) into one JSON the bambu-studio CLI can load:
#   python3 bambu_flatten_profile.py machine "Bambu Lab A1 0.4 nozzle" m.json "change_filament_gcode=M400 U1"
# Used 2026-10-18 to make bambu_A1_project_settings.config (CLI --export-3mf, then flush_volumes_matrix fixed to 2x2).
import json, os, sys
P = "/path/to/bambustudio/resources/profiles/BBL"   # Bambu Studio's bundled system profiles
def find(kind, name):
    fn = os.path.join(P, kind, name + ".json")
    if os.path.exists(fn): return fn
    for root, _, files in os.walk(os.path.join(P, kind)):
        if name + ".json" in files: return os.path.join(root, name + ".json")
    raise FileNotFoundError(kind + "/" + name)
def flat(kind, name):
    d = json.load(open(find(kind, name)))
    out = flat(kind, d["inherits"]) if d.get("inherits") else {}
    for inc in d.get("include", []):
        t = json.load(open(find(kind, inc)))
        out.update({k: v for k, v in t.items() if k not in ("type", "name", "from", "instantiation", "inherits", "include", "setting_id")})
    out.update({k: v for k, v in d.items() if k not in ("include",)})
    return out
kind, name, outfn = sys.argv[1], sys.argv[2], sys.argv[3]
d = flat(kind, name); d.pop("inherits", None); d["from"] = "User"; d["instantiation"] = "true"; d["name"] = name
for kv in sys.argv[4:]:
    k, v = kv.split("=", 1); d[k] = v
json.dump(d, open(outfn, "w"), indent=1)
print(outfn, len(d), "keys")
