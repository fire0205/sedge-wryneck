"""Final-module finish: fill 0.999 and a width/height stretch, applied to the finished module text only.

The module keeps its own fit (centred, longest side at the fill). After that fit, the x and y sides are scaled up to
1.25 times, never past the longest side, and the object is re-centred. Depth (z) is not stretched. If the result is
larger than the fill it is scaled back uniformly. The object stays centred at the origin inside the unit cube.
Any module that does not have the expected generate() layout is returned unchanged.
"""

_EXPORT = "export default function generate(THREE) {\n"
_FILL = "    const scale = 0.99 / extent;\n"
_FILL_NEW = "    const scale = 0.999 / extent;\n"
_END = "  return root;\n}"
_STRETCH = """  {
    root.updateMatrixWorld(true);
    const b2 = new THREE.Box3().setFromObject(root);
    const s2 = b2.getSize(new THREE.Vector3());
    const e2 = Math.max(s2.x, s2.y, s2.z);
    if (e2 > 0 && Number.isFinite(e2)) {
      const f = function (v) { return Math.min(1.25, e2 / Math.max(v, 1e-9)); };
      root.scale.set(root.scale.x * f(s2.x), root.scale.y * f(s2.y), root.scale.z * 1);
      root.updateMatrixWorld(true);
      let b3 = new THREE.Box3().setFromObject(root);
      const e3 = Math.max(...b3.getSize(new THREE.Vector3()).toArray());
      if (e3 > 0.999) { root.scale.multiplyScalar(0.999 / e3); root.updateMatrixWorld(true); b3 = new THREE.Box3().setFromObject(root); }
      root.position.sub(b3.getCenter(new THREE.Vector3()));
    }
  }
"""


def finish(source: str | None) -> str | None:
    if not source or source.count(_EXPORT) != 1:
        return source
    at = source.find(_EXPORT)
    head, tail = source[:at], source[at:]
    if tail.count(_FILL) == 1:
        tail = tail.replace(_FILL, _FILL_NEW, 1)
    if tail.count(_FILL_NEW) != 1 or not tail.rstrip().endswith(_END):
        return source
    end = tail.rfind(_END)
    return head + tail[:end] + _STRETCH + tail[end:]
