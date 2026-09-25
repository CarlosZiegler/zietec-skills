#!/usr/bin/env python3
"""Read-only STL screening. A screen_pass is not print or slice approval."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import sys
import tempfile


def read_stl(path):
    data = Path(path).read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from('<I', data, 80)[0]
        if len(data) == 84 + 50 * count:
            triangles = []
            for offset in range(84, len(data), 50):
                values = struct.unpack_from('<12fH', data, offset)
                triangles.append(tuple(tuple(values[i:i + 3]) for i in (3, 6, 9)))
            return triangles, hashlib.sha256(data).hexdigest()
    # Binary headers can begin with "solid"; exact binary length takes priority.
    text = data.decode('ascii')
    lines = [line.strip().split() for line in text.splitlines() if line.strip()]
    triangles = []
    i = 0
    while i < len(lines):
        if lines[i][0].lower() != 'solid':
            raise ValueError('Not a complete ASCII STL or exact-length binary STL')
        i += 1
        while i < len(lines) and lines[i][0].lower() == 'facet':
            if len(lines[i]) != 5 or lines[i][1].lower() != 'normal':
                raise ValueError('Malformed facet normal')
            if i + 6 >= len(lines) or lines[i + 1] != ['outer', 'loop']:
                raise ValueError('Malformed facet loop')
            points = lines[i + 2:i + 5]
            if any(len(row) != 4 or row[0] != 'vertex' for row in points):
                raise ValueError('Expected exactly three vertices per facet')
            if lines[i + 5] != ['endloop'] or lines[i + 6] != ['endfacet']:
                raise ValueError('Incomplete facet')
            triangles.append(tuple(tuple(map(float, row[1:])) for row in points))
            i += 7
        if i >= len(lines) or lines[i][0].lower() != 'endsolid':
            raise ValueError('Missing endsolid')
        i += 1
    if not lines:
        raise ValueError('Empty STL')
    return triangles, hashlib.sha256(data).hexdigest()


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def require_finite_measurements(value):
    if isinstance(value, dict):
        for child in value.values():
            require_finite_measurements(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            require_finite_measurements(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Derived measurement is not finite; check coordinates and unit scale')


def audit_triangles(triangles, unit_scale=1.0, bed_z=0.0, z_tolerance=0.001):
    if not math.isfinite(unit_scale) or unit_scale <= 0:
        raise ValueError('unit_scale must be positive and finite')
    if not math.isfinite(bed_z) or not math.isfinite(z_tolerance) or z_tolerance <= 0:
        raise ValueError('bed_z must be finite; z_tolerance must be positive and finite')
    triangles = [tuple(tuple(v * unit_scale for v in p) for p in tri) for tri in triangles]
    if not triangles or any(not math.isfinite(v) for tri in triangles for p in tri for v in p):
        raise ValueError('STL must contain triangles with finite coordinates')
    points = [p for tri in triangles for p in tri]
    low = tuple(min(p[i] for p in points) for i in range(3))
    high = tuple(max(p[i] for p in points) for i in range(3))
    edges = defaultdict(list)
    duplicate_faces = Counter(tuple(sorted(tri)) for tri in triangles)
    parents = list(range(len(triangles)))

    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    contact = 0.0
    horizontal = {}
    downward_area = 0.0
    downward_z = []
    degenerate = 0
    for i, tri in enumerate(triangles):
        a, b, c = tri
        normal = cross(subtract(b, a), subtract(c, a))
        norm = math.hypot(*normal)
        require_finite_measurements(norm)
        if norm <= 1e-12:
            degenerate += 1
            continue
        for u, v in [(a, b), (b, c), (c, a)]:
            key = tuple(sorted((u, v)))
            if edges[key]:
                parents[root(i)] = root(edges[key][0][0])
            edges[key].append((i, 1 if u < v else -1))
        z_min, z_max = min(p[2] for p in tri), max(p[2] for p in tri)
        if normal[2] / norm < -1e-6:
            if max(abs(z_min - bed_z), abs(z_max - bed_z)) <= z_tolerance:
                contact += norm / 2
            if z_max > bed_z + z_tolerance:
                downward_area += norm / 2
                downward_z.extend((z_min, z_max))
                if z_max - z_min <= z_tolerance:
                    level = round((z_min + z_max) / 2 / z_tolerance)
                    group = horizontal.setdefault(level, {'area_mm2': 0.0, 'z_min_mm': z_min,
                                                          'z_max_mm': z_max, 'triangles': 0})
                    group['area_mm2'] += norm / 2
                    group['z_min_mm'] = min(group['z_min_mm'], z_min)
                    group['z_max_mm'] = max(group['z_max_mm'], z_max)
                    group['triangles'] += 1
    shells = defaultdict(list)
    for i in range(len(triangles)):
        shells[root(i)].append(i)
    shell_report = []
    for ids in shells.values():
        reference = triangles[ids[0]][0]
        volume = math.fsum(dot(subtract(a, reference), cross(subtract(b, reference), subtract(c, reference))) / 6
                           for i in ids for a, b, c in [triangles[i]])
        vertices = [p for i in ids for p in triangles[i]]
        shell_low = tuple(min(p[axis] for p in vertices) for axis in range(3))
        shell_high = tuple(max(p[axis] for p in vertices) for axis in range(3))
        shell_report.append({'triangles': len(ids), 'signed_volume_mm3': volume,
                             'z_min_mm': shell_low[2], 'z_max_mm': shell_high[2],
                             'bounds_mm': {'min': shell_low, 'max': shell_high}})
    possible_cavities, bad_volumes = [], []
    for shell in shell_report:
        if shell['signed_volume_mm3'] > 0:
            continue
        # A closed cavity has a negative boundary shell. Bounding boxes only
        # identify candidates, never prove nesting or authorize a mesh repair.
        enclosed_candidate = shell['signed_volume_mm3'] < 0 and any(
            outer['signed_volume_mm3'] > 0 and all(
                outer['bounds_mm']['min'][axis] <= shell['bounds_mm']['min'][axis]
                and shell['bounds_mm']['max'][axis] <= outer['bounds_mm']['max'][axis]
                for axis in range(3)
            ) for outer in shell_report
        )
        (possible_cavities if enclosed_candidate else bad_volumes).append(shell)
    nonmanifold = sum(len(uses) != 2 for uses in edges.values())
    winding = sum(len(uses) == 2 and sum(sign for _, sign in uses) != 0 for uses in edges.values())
    duplicates = sum(count - 1 for count in duplicate_faces.values())
    blocking = []
    if nonmanifold:
        blocking.append('open_or_nonmanifold_edges')
    if winding:
        blocking.append('inconsistent_winding')
    if duplicates or degenerate:
        blocking.append('duplicate_or_degenerate_faces')
    if bad_volumes:
        blocking.append('nonpositive_shell_volume')
    if low[2] < bed_z - z_tolerance:
        blocking.append('geometry_below_bed')
    review = []
    if low[2] > bed_z + z_tolerance:
        review.append('whole_object_above_bed')
    if contact <= 0:
        review.append('no_planar_bed_contact')
    if len(shell_report) > 1:
        review.append('multiple_shells_check_each')
    if possible_cavities:
        review.append('negative_shell_verify_cavity_or_winding')
    if downward_area > 0:
        review.append('elevated_downward_faces_check_support_or_bridge')
    report = {
        'status': 'blocked' if blocking else 'review_required' if review else 'screen_pass',
        'blocking_findings': blocking, 'review_findings': review,
        'dimensions_mm': [high[i] - low[i] for i in range(3)],
        'bounds_mm': {'min': low, 'max': high}, 'triangles': len(triangles),
        'nonmanifold_edges': nonmanifold, 'inconsistent_winding_edges': winding,
        'duplicate_triangles': duplicates, 'degenerate_triangles': degenerate,
        'shells': shell_report, 'planar_bed_contact_area_mm2': contact,
        'elevated_downward_area_mm2': downward_area,
        'elevated_downward_z_range_mm': [min(downward_z), max(downward_z)] if downward_z else None,
        'horizontal_undersides_above_bed': [horizontal[k] for k in sorted(horizontal)],
        'convention': {'unit_scale_to_mm': unit_scale, 'bed_z_mm': bed_z,
                       'z_tolerance_mm': z_tolerance, 'topology_vertices': 'exact coordinates; no welding'},
        'slice_review': 'required', 'physical_print': 'not_verified',
        'not_checked': ['self_intersection', 'vertex_manifoldness', 'exact_shell_nesting', 'wall_thickness',
                        'bridge_anchoring_or_capacity', 'stability_or_adhesion',
                        'strength', 'inter_object_collisions', 'slicer_support_coverage'],
    }
    require_finite_measurements(report)
    return report


def write_report(path, text):
    # Replace the directory entry instead of following a late-created symlink.
    # Keep the previous report intact if writing or replacement fails.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix=f'.{path.name}.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', type=Path, nargs='+')
    parser.add_argument('--unit-scale', type=float, default=1.0, help='Multiply STL coordinates to mm')
    parser.add_argument('--bed-z', type=float, default=0.0, help='Print bed height, in mm after scaling')
    parser.add_argument('--z-tolerance', type=float, default=0.001, help='Plane tolerance in mm (default .001)')
    parser.add_argument('--output', type=Path, help='Write JSON report, never over an input STL')
    args = parser.parse_args(argv)
    if args.output:
        for path in args.files:
            if args.output.resolve() == path.resolve() or (
                args.output.exists() and path.exists() and args.output.samefile(path)
            ):
                parser.error('Output must not overwrite an input STL')
    reports = []
    code = 0
    for path in args.files:
        try:
            triangles, digest = read_stl(path)
            report = audit_triangles(triangles, args.unit_scale, args.bed_z, args.z_tolerance)
            reports.append({'file': str(path), 'sha256': digest, **report})
            if report['status'] != 'screen_pass' and code != 1:
                code = 2
        except (OSError, ValueError, ArithmeticError, struct.error) as exc:
            reports.append({'file': str(path), 'status': 'input_error', 'error': str(exc)})
            code = 1
    result = json.dumps({'schema_version': 1, 'files': reports}, indent=2, allow_nan=False)
    try:
        if args.output:
            write_report(args.output, result + '\n')
        else:
            print(result)
    except OSError as exc:
        print(f'Cannot write report: {exc}', file=sys.stderr)
        return 1
    return code


if __name__ == '__main__':
    sys.exit(main())
