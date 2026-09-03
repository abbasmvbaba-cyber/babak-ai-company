#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a small, self-contained glTF 2.0/GLB character blocking asset.

This is intentionally dependency-free so the repository can be rebuilt without
installing Blender or a Python package. It creates a skinned humanoid mannequin
with a named skeleton, simple materials, facial morph targets, interaction props,
and animation clips. The generated GLB is a controllable technical prototype;
the final likeness, PBR textures and production VRM export still belong to the
next art/rigging pass.
"""
from __future__ import annotations

import json
import math
import struct
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "babak-moradvand-rigged.glb"
MANIFEST = HERE / "babak-moradvand-rig-manifest.json"

# glTF constants.
FLOAT = 5126
UNSIGNED_SHORT = 5123
UNSIGNED_INT = 5125
ARRAY_BUFFER = 34962
ELEMENT_ARRAY_BUFFER = 34963


def v_add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def v_sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def v_mul(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def norm(a):
    length = math.sqrt(dot(a, a))
    return [0.0, 0.0, 0.0] if length < 1e-8 else v_mul(a, 1.0 / length)


def quat_euler(x_deg=0.0, y_deg=0.0, z_deg=0.0):
    """XYZ Euler degrees to a glTF quaternion [x, y, z, w]."""
    x, y, z = [math.radians(value) * 0.5 for value in (x_deg, y_deg, z_deg)]
    cx, cy, cz = math.cos(x), math.cos(y), math.cos(z)
    sx, sy, sz = math.sin(x), math.sin(y), math.sin(z)
    return [
        sx * cy * cz - cx * sy * sz,
        cx * sy * cz + sx * cy * sz,
        cx * cy * sz - sx * sy * cz,
        cx * cy * cz + sx * sy * sz,
    ]


def identity_quat():
    return [0.0, 0.0, 0.0, 1.0]


def mat4_translation(t):
    # glTF matrices are column-major.
    return [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, t[0], t[1], t[2], 1.0]


class GLBBuilder:
    def __init__(self):
        self.binary = bytearray()
        self.gltf = {
            "asset": {"version": "2.0", "generator": "Babak AI Company dependency-free rig builder"},
            "scene": 0,
            "scenes": [{"nodes": []}],
            "nodes": [],
            "meshes": [],
            "materials": [],
            "skins": [],
            "accessors": [],
            "bufferViews": [],
            "buffers": [],
            "animations": [],
        }

    def _align(self):
        while len(self.binary) % 4:
            self.binary.append(0)

    def add_blob(self, blob: bytes, target: int | None = None) -> int:
        self._align()
        offset = len(self.binary)
        self.binary.extend(blob)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(blob)}
        if target is not None:
            view["target"] = target
        self.gltf["bufferViews"].append(view)
        return len(self.gltf["bufferViews"]) - 1

    def add_accessor(self, values, component_type: int, accessor_type: str, target: int | None = None, *, minmax=True, name=None):
        component_count = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}[accessor_type]
        if accessor_type == "SCALAR":
            rows = [[value] for value in values]
        else:
            rows = [list(row) for row in values]
        flat = [value for row in rows for value in row]
        if component_type == FLOAT:
            blob = struct.pack("<" + "f" * len(flat), *[float(value) for value in flat])
        elif component_type == UNSIGNED_SHORT:
            blob = struct.pack("<" + "H" * len(flat), *[int(value) for value in flat])
        elif component_type == UNSIGNED_INT:
            blob = struct.pack("<" + "I" * len(flat), *[int(value) for value in flat])
        else:
            raise ValueError(component_type)
        view_index = self.add_blob(blob, target)
        accessor = {
            "bufferView": view_index,
            "componentType": component_type,
            "count": len(rows),
            "type": accessor_type,
        }
        if name:
            accessor["name"] = name
        if minmax and rows and accessor_type != "MAT4":
            accessor["min"] = [min(row[i] for row in rows) for i in range(component_count)]
            accessor["max"] = [max(row[i] for row in rows) for i in range(component_count)]
        self.gltf["accessors"].append(accessor)
        return len(self.gltf["accessors"]) - 1

    def add_material(self, name, color, *, metallic=0.0, roughness=0.6, alpha_mode=None, alpha_cutoff=None):
        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [*color, 1.0],
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
        }
        if alpha_mode:
            material["alphaMode"] = alpha_mode
        if alpha_cutoff is not None:
            material["alphaCutoff"] = alpha_cutoff
        self.gltf["materials"].append(material)
        return len(self.gltf["materials"]) - 1

    def add_mesh(self, mesh):
        self.gltf["meshes"].append(mesh)
        return len(self.gltf["meshes"]) - 1

    def add_node(self, node):
        self.gltf["nodes"].append(node)
        return len(self.gltf["nodes"]) - 1

    def finish(self, path: Path):
        self.gltf["buffers"] = [{"byteLength": len(self.binary)}]
        json_bytes = json.dumps(self.gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        while len(json_bytes) % 4:
            json_bytes += b" "
        binary = bytes(self.binary)
        while len(binary) % 4:
            binary += b"\0"
        total_length = 12 + 8 + len(json_bytes) + 8 + len(binary)
        header = struct.pack("<4sII", b"glTF", 2, total_length)
        chunks = struct.pack("<I4s", len(json_bytes), b"JSON") + json_bytes
        chunks += struct.pack("<I4s", len(binary), b"BIN\0") + binary
        path.write_bytes(header + chunks)


class SkinnedPrimitive:
    def __init__(self, material):
        self.material = material
        self.positions = []
        self.normals = []
        self.joints = []
        self.weights = []
        self.indices = []

    def vertex(self, position, normal, joint):
        self.positions.append([float(x) for x in position])
        self.normals.append([float(x) for x in normal])
        self.joints.append([joint, 0, 0, 0])
        self.weights.append([1.0, 0.0, 0.0, 0.0])
        return len(self.positions) - 1

    def triangle(self, a, b, c):
        self.indices.extend([a, b, c])

    def quad(self, a, b, c, d):
        self.triangle(a, b, c)
        self.triangle(a, c, d)


class StaticPrimitive:
    def __init__(self, material):
        self.material = material
        self.positions = []
        self.normals = []
        self.indices = []

    def vertex(self, position, normal):
        self.positions.append([float(x) for x in position])
        self.normals.append([float(x) for x in normal])
        return len(self.positions) - 1

    def triangle(self, a, b, c):
        self.indices.extend([a, b, c])

    def quad(self, a, b, c, d):
        self.triangle(a, b, c)
        self.triangle(a, c, d)


def add_box(builder, center, size, joint=None):
    cx, cy, cz = center
    sx, sy, sz = [value * 0.5 for value in size]
    corners = [
        [cx - sx, cy - sy, cz - sz], [cx + sx, cy - sy, cz - sz], [cx + sx, cy + sy, cz - sz], [cx - sx, cy + sy, cz - sz],
        [cx - sx, cy - sy, cz + sz], [cx + sx, cy - sy, cz + sz], [cx + sx, cy + sy, cz + sz], [cx - sx, cy + sy, cz + sz],
    ]
    faces = [
        ((0, 3, 2, 1), [0, 0, -1]), ((4, 5, 6, 7), [0, 0, 1]),
        ((0, 1, 5, 4), [0, -1, 0]), ((3, 7, 6, 2), [0, 1, 0]),
        ((1, 2, 6, 5), [1, 0, 0]), ((0, 4, 7, 3), [-1, 0, 0]),
    ]
    for indices, normal in faces:
        ids = [builder.vertex(corners[index], normal, joint) if joint is not None else builder.vertex(corners[index], normal) for index in indices]
        builder.quad(*ids)


def add_segment(builder, a, b, radius_a, radius_b, joint=None, sides=8):
    axis = norm(v_sub(b, a))
    reference = [0.0, 1.0, 0.0] if abs(axis[1]) < 0.9 else [1.0, 0.0, 0.0]
    u = norm(cross(axis, reference))
    v = norm(cross(axis, u))
    rings = []
    for center, radius in ((a, radius_a), (b, radius_b)):
        ring = []
        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            radial = v_add(v_mul(u, math.cos(angle) * radius), v_mul(v, math.sin(angle) * radius))
            position = v_add(center, radial)
            normal = norm(radial)
            ring.append(builder.vertex(position, normal, joint) if joint is not None else builder.vertex(position, normal))
        rings.append(ring)
    for i in range(sides):
        j = (i + 1) % sides
        builder.quad(rings[0][i], rings[0][j], rings[1][j], rings[1][i])
    if joint is not None:
        start = builder.vertex(a, v_mul(axis, -1.0), joint)
        end = builder.vertex(b, axis, joint)
    else:
        start = builder.vertex(a, v_mul(axis, -1.0))
        end = builder.vertex(b, axis)
    for i in range(sides):
        j = (i + 1) % sides
        builder.triangle(start, rings[0][j], rings[0][i])
        builder.triangle(end, rings[1][i], rings[1][j])


def add_uv_sphere(builder, center, radii, joint=None, segments=14, rings=8):
    cx, cy, cz = center
    rx, ry, rz = radii
    rows = []
    for ring in range(rings + 1):
        phi = math.pi * ring / rings
        row = []
        for segment in range(segments):
            theta = 2.0 * math.pi * segment / segments
            unit = [math.sin(phi) * math.cos(theta), math.cos(phi), math.sin(phi) * math.sin(theta)]
            position = [cx + rx * unit[0], cy + ry * unit[1], cz + rz * unit[2]]
            normal = norm([unit[0] / max(rx, 1e-6), unit[1] / max(ry, 1e-6), unit[2] / max(rz, 1e-6)])
            row.append(builder.vertex(position, normal, joint) if joint is not None else builder.vertex(position, normal))
        rows.append(row)
    for ring in range(rings):
        for segment in range(segments):
            next_segment = (segment + 1) % segments
            builder.quad(rows[ring][segment], rows[ring][next_segment], rows[ring + 1][next_segment], rows[ring + 1][segment])


def add_cylinder(builder, center, radius, height, material, sides=16):
    cx, cy, cz = center
    bottom = []
    top = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        x, z = math.cos(angle) * radius, math.sin(angle) * radius
        bottom.append(builder.vertex([cx + x, cy - height / 2, cz + z], [0, -1, 0]))
        top.append(builder.vertex([cx + x, cy + height / 2, cz + z], [0, 1, 0]))
    for i in range(sides):
        j = (i + 1) % sides
        builder.quad(bottom[i], bottom[j], top[j], top[i])
    bcenter = builder.vertex([cx, cy - height / 2, cz], [0, -1, 0])
    tcenter = builder.vertex([cx, cy + height / 2, cz], [0, 1, 0])
    for i in range(sides):
        j = (i + 1) % sides
        builder.triangle(bcenter, bottom[j], bottom[i])
        builder.triangle(tcenter, top[i], top[j])


def world_positions(bones, nodes):
    result = {}

    def visit(index, parent):
        local = nodes[index].get("translation", [0.0, 0.0, 0.0])
        position = v_add(parent, local)
        result[index] = position
        for child in nodes[index].get("children", []):
            visit(child, position)

    visit(bones["Hips"], [0.0, 0.0, 0.0])
    return result


def make_skinned_mesh(builder: GLBBuilder, primitives, skin_index, name, joint_map=None):
    gltf_primitives = []
    for primitive in primitives:
        position = builder.add_accessor(primitive.positions, FLOAT, "VEC3", ARRAY_BUFFER, name=f"{name}_{primitive.material}_positions")
        normal = builder.add_accessor(primitive.normals, FLOAT, "VEC3", ARRAY_BUFFER, name=f"{name}_{primitive.material}_normals")
        # JOINTS_0 stores indices into skins[skin_index].joints, not glTF node indices.
        joint_values = primitive.joints if joint_map is None else [[joint_map.get(value, 0) for value in row] for row in primitive.joints]
        joints = builder.add_accessor(joint_values, UNSIGNED_SHORT, "VEC4", ARRAY_BUFFER, name=f"{name}_{primitive.material}_joints")
        weights = builder.add_accessor(primitive.weights, FLOAT, "VEC4", ARRAY_BUFFER, name=f"{name}_{primitive.material}_weights")
        index_component = UNSIGNED_SHORT if len(primitive.positions) < 65536 else UNSIGNED_INT
        indices = builder.add_accessor(primitive.indices, index_component, "SCALAR", ELEMENT_ARRAY_BUFFER, name=f"{name}_{primitive.material}_indices")
        gltf_primitives.append({
            "attributes": {"POSITION": position, "NORMAL": normal, "JOINTS_0": joints, "WEIGHTS_0": weights},
            "indices": indices,
            "material": primitive.material,
        })
    return builder.add_mesh({"name": name, "primitives": gltf_primitives, "extras": {"skin": skin_index}})


def make_static_mesh(builder: GLBBuilder, primitives, name):
    gltf_primitives = []
    for primitive in primitives:
        position = builder.add_accessor(primitive.positions, FLOAT, "VEC3", ARRAY_BUFFER, name=f"{name}_{primitive.material}_positions")
        normal = builder.add_accessor(primitive.normals, FLOAT, "VEC3", ARRAY_BUFFER, name=f"{name}_{primitive.material}_normals")
        index_component = UNSIGNED_SHORT if len(primitive.positions) < 65536 else UNSIGNED_INT
        indices = builder.add_accessor(primitive.indices, index_component, "SCALAR", ELEMENT_ARRAY_BUFFER, name=f"{name}_{primitive.material}_indices")
        gltf_primitives.append({"attributes": {"POSITION": position, "NORMAL": normal}, "indices": indices, "material": primitive.material})
    return builder.add_mesh({"name": name, "primitives": gltf_primitives})


def add_animation(builder: GLBBuilder, name, duration, channels, *, loop=False, description=""):
    samplers = []
    gltf_channels = []
    for channel in channels:
        times = channel["times"]
        values = channel["values"]
        input_accessor = builder.add_accessor(times, FLOAT, "SCALAR", name=f"{name}_{channel['path']}_time")
        if channel["path"] == "weights":
            flattened = [value for row in values for value in row]
            output_accessor = builder.add_accessor(flattened, FLOAT, "SCALAR", name=f"{name}_weights", minmax=False)
        else:
            output_type = "VEC3" if channel["path"] == "translation" else "VEC4"
            output_accessor = builder.add_accessor(values, FLOAT, output_type, name=f"{name}_{channel['path']}")
        sampler_index = len(samplers)
        samplers.append({"input": input_accessor, "output": output_accessor, "interpolation": channel.get("interpolation", "LINEAR")})
        gltf_channels.append({"sampler": sampler_index, "target": {"node": channel["node"], "path": channel["path"]}})
    animation = {"name": name, "samplers": samplers, "channels": gltf_channels, "extras": {"duration_seconds": duration, "loop": loop, "description": description}}
    builder.gltf["animations"].append(animation)


def main():
    builder = GLBBuilder()

    material_ids = {
        "suit": builder.add_material("Navy Pinstripe Suit", [0.035, 0.07, 0.16], metallic=0.05, roughness=0.36),
        "suit_highlight": builder.add_material("Suit Pinstripe Highlight", [0.10, 0.18, 0.34], metallic=0.05, roughness=0.38),
        "skin": builder.add_material("Warm Skin", [0.68, 0.34, 0.22], roughness=0.52),
        "shirt": builder.add_material("White Shirt", [0.92, 0.94, 0.96], roughness=0.42),
        "gold": builder.add_material("Gold Details", [0.72, 0.42, 0.08], metallic=0.62, roughness=0.25),
        "hair": builder.add_material("Buzz Cut Hair", [0.025, 0.018, 0.014], roughness=0.48),
        "glass": builder.add_material("Warm Amber Glass", [0.72, 0.34, 0.035], metallic=0.1, roughness=0.18, alpha_mode="BLEND"),
        "eye": builder.add_material("Eye White", [0.96, 0.96, 0.92], roughness=0.3),
        "pupil": builder.add_material("Pupil", [0.008, 0.006, 0.004], roughness=0.2),
        "shoe": builder.add_material("Polished Brown Shoes", [0.12, 0.035, 0.015], metallic=0.08, roughness=0.22),
        "paper": builder.add_material("Document Paper", [0.82, 0.86, 0.92], roughness=0.55),
        "coffee": builder.add_material("Coffee Mug", [0.07, 0.10, 0.16], metallic=0.15, roughness=0.3),
    }

    # Root and skeleton. The rest pose is an approximately 1.88 m human scale.
    root = builder.add_node({
        "name": "Babak_Moradvand_Root",
        "children": [],
        "extras": {
            "character_id": "BAC-0001",
            "height_cm": 188,
            "coordinate_system": "Y-up, +Z forward",
            "rig_type": "humanoid-skinned-prototype",
        },
    })
    builder.gltf["scenes"][0]["nodes"].append(root)
    bones = {}
    bone_parents = {}

    def add_bone(name, parent_name, translation, humanoid_name):
        node = {"name": name, "translation": translation, "children": [], "extras": {"humanoidBone": humanoid_name}}
        index = builder.add_node(node)
        bones[name] = index
        bone_parents[name] = parent_name
        if parent_name is None:
            builder.gltf["nodes"][root]["children"].append(index)
        else:
            builder.gltf["nodes"][bones[parent_name]]["children"].append(index)
        return index

    add_bone("Hips", None, [0.0, 0.83, 0.0], "hips")
    add_bone("Spine", "Hips", [0.0, 0.20, 0.0], "spine")
    add_bone("Chest", "Spine", [0.0, 0.20, 0.0], "chest")
    add_bone("Neck", "Chest", [0.0, 0.17, 0.0], "neck")
    add_bone("Head", "Neck", [0.0, 0.16, 0.0], "head")
    add_bone("Jaw", "Head", [0.0, -0.08, 0.13], "jaw")
    add_bone("LeftEye", "Head", [-0.078, 0.14, 0.17], "leftEye")
    add_bone("RightEye", "Head", [0.078, 0.14, 0.17], "rightEye")
    add_bone("LeftShoulder", "Chest", [0.20, 0.11, 0.0], "leftShoulder")
    add_bone("LeftUpperArm", "LeftShoulder", [0.16, 0.0, 0.0], "leftUpperArm")
    add_bone("LeftLowerArm", "LeftUpperArm", [0.28, -0.07, 0.0], "leftLowerArm")
    add_bone("LeftHand", "LeftLowerArm", [0.23, 0.0, 0.0], "leftHand")
    add_bone("RightShoulder", "Chest", [-0.20, 0.11, 0.0], "rightShoulder")
    add_bone("RightUpperArm", "RightShoulder", [-0.16, 0.0, 0.0], "rightUpperArm")
    add_bone("RightLowerArm", "RightUpperArm", [-0.28, -0.07, 0.0], "rightLowerArm")
    add_bone("RightHand", "RightLowerArm", [-0.23, 0.0, 0.0], "rightHand")
    add_bone("LeftUpperLeg", "Hips", [-0.12, -0.40, 0.0], "leftUpperLeg")
    add_bone("LeftLowerLeg", "LeftUpperLeg", [0.0, -0.40, 0.0], "leftLowerLeg")
    add_bone("LeftFoot", "LeftLowerLeg", [0.0, -0.03, 0.08], "leftFoot")
    add_bone("LeftToes", "LeftFoot", [0.0, 0.0, 0.15], "leftToes")
    add_bone("RightUpperLeg", "Hips", [0.12, -0.40, 0.0], "rightUpperLeg")
    add_bone("RightLowerLeg", "RightUpperLeg", [0.0, -0.40, 0.0], "rightLowerLeg")
    add_bone("RightFoot", "RightLowerLeg", [0.0, -0.03, 0.08], "rightFoot")
    add_bone("RightToes", "RightFoot", [0.0, 0.0, 0.15], "rightToes")

    world_by_index = world_positions(bones, builder.gltf["nodes"])
    positions = {name: world_by_index[index] for name, index in bones.items()}
    # glTF skin weights reference the ordinal slot in skins[0].joints.
    skin_joint_indices = {node_index: slot for slot, node_index in enumerate(bones.values())}

    # Build the skinned body, grouped by material.
    body_primitives = {name: SkinnedPrimitive(material_id) for name, material_id in material_ids.items()}
    suit = body_primitives["suit"]
    highlight = body_primitives["suit_highlight"]
    skin = body_primitives["skin"]
    shirt = body_primitives["shirt"]
    gold = body_primitives["gold"]
    hair = body_primitives["hair"]
    glass = body_primitives["glass"]
    eye = body_primitives["eye"]
    pupil = body_primitives["pupil"]
    shoe = body_primitives["shoe"]

    add_box(suit, [0.0, 0.86, 0.0], [0.34, 0.22, 0.25], bones["Hips"])
    add_box(suit, [0.0, 1.07, 0.0], [0.43, 0.30, 0.28], bones["Spine"])
    add_box(suit, [0.0, 1.28, 0.0], [0.48, 0.28, 0.30], bones["Chest"])
    add_box(highlight, [0.0, 1.28, 0.155], [0.25, 0.24, 0.025], bones["Chest"])
    add_box(shirt, [0.0, 1.43, 0.16], [0.22, 0.20, 0.035], bones["Chest"])
    add_box(gold, [0.0, 1.28, 0.175], [0.045, 0.27, 0.025], bones["Chest"])
    add_box(gold, [0.0, 1.28, 0.19], [0.19, 0.025, 0.025], bones["Chest"])

    for side, sign in (("Left", 1.0), ("Right", -1.0)):
        add_segment(suit, positions[f"{side}UpperLeg"], positions[f"{side}LowerLeg"], 0.115, 0.095, bones[f"{side}UpperLeg"])
        add_segment(suit, positions[f"{side}LowerLeg"], positions[f"{side}Foot"], 0.095, 0.075, bones[f"{side}LowerLeg"])
        add_box(shoe, v_add(positions[f"{side}Foot"], [0.0, -0.025, 0.09]), [0.18, 0.095, 0.30], bones[f"{side}Foot"])
        add_box(shoe, v_add(positions[f"{side}Toes"], [0.0, -0.025, 0.02]), [0.18, 0.075, 0.14], bones[f"{side}Toes"])
        add_segment(suit, positions[f"{side}UpperArm"], positions[f"{side}LowerArm"], 0.075, 0.065, bones[f"{side}UpperArm"])
        add_segment(suit, positions[f"{side}LowerArm"], positions[f"{side}Hand"], 0.065, 0.052, bones[f"{side}LowerArm"])
        add_box(shirt, v_add(positions[f"{side}Hand"], [0.0, 0.0, 0.0]), [0.12, 0.065, 0.075], bones[f"{side}LowerArm"])
        add_uv_sphere(skin, positions[f"{side}Hand"], [0.065, 0.08, 0.065], bones[f"{side}Hand"], segments=10, rings=5)

    add_segment(skin, positions["Neck"], positions["Head"], 0.075, 0.12, bones["Neck"])
    # Hair cap, sideburn hints and ears follow the head bone.
    add_uv_sphere(hair, [0.0, 1.70, -0.005], [0.205, 0.12, 0.18], bones["Head"], segments=14, rings=6)
    add_box(hair, [0.0, 1.78, -0.01], [0.31, 0.08, 0.28], bones["Head"])
    add_uv_sphere(skin, [0.205, 1.67, 0.0], [0.035, 0.07, 0.06], bones["Head"], segments=8, rings=4)
    add_uv_sphere(skin, [-0.205, 1.67, 0.0], [0.035, 0.07, 0.06], bones["Head"], segments=8, rings=4)
    # Eyes and simple yellow glasses, placed toward +Z (the face direction).
    for x in (-0.078, 0.078):
        eye_bone = "LeftEye" if x < 0 else "RightEye"
        add_uv_sphere(eye, [x, 1.70, 0.17], [0.052, 0.036, 0.022], bones[eye_bone], segments=10, rings=4)
        add_uv_sphere(pupil, [x, 1.70, 0.193], [0.018, 0.019, 0.008], bones[eye_bone], segments=8, rings=3)
        add_box(glass, [x, 1.70, 0.212], [0.12, 0.065, 0.012], bones["Head"])
    add_box(gold, [0.0, 1.70, 0.214], [0.035, 0.018, 0.014], bones["Head"])
    add_box(gold, [0.0, 1.70, 0.205], [0.23, 0.012, 0.012], bones["Head"])

    body_mesh = make_skinned_mesh(builder, [primitive for primitive in body_primitives.values() if primitive.positions], 0, "Babak_Body_Skinned", joint_map=skin_joint_indices)
    body_node = builder.add_node({"name": "Body_Skinned", "mesh": body_mesh, "skin": 0, "extras": {"role": "rigged body and suit"}})
    builder.gltf["nodes"][root]["children"].append(body_node)

    # A separate face mesh carries four simple production-facing blendshape channels.
    face_primitive = SkinnedPrimitive(material_ids["skin"])
    add_uv_sphere(face_primitive, [0.0, 1.67, 0.025], [0.19, 0.23, 0.175], bones["Head"], segments=16, rings=10)
    face_positions = [list(p) for p in face_primitive.positions]
    target_names = ["mouthOpen", "smile", "blinkLeft", "blinkRight"]
    target_arrays = []
    for target_name in target_names:
        deltas = []
        for p in face_positions:
            dx = dy = dz = 0.0
            if target_name == "mouthOpen" and p[1] < 1.64 and p[2] > 0.12:
                dy = -0.018
            elif target_name == "smile" and 1.61 < p[1] < 1.68 and p[2] > 0.12:
                dy = 0.008
                dz = 0.004
            elif target_name == "blinkLeft" and -0.16 < p[0] < -0.01 and 1.675 < p[1] < 1.73 and p[2] > 0.13:
                dy = -0.014
            elif target_name == "blinkRight" and 0.01 < p[0] < 0.16 and 1.675 < p[1] < 1.73 and p[2] > 0.13:
                dy = -0.014
            deltas.append([dx, dy, dz])
        target_arrays.append(deltas)
    face_position = builder.add_accessor(face_primitive.positions, FLOAT, "VEC3", ARRAY_BUFFER, name="Face_POSITION")
    face_normal = builder.add_accessor(face_primitive.normals, FLOAT, "VEC3", ARRAY_BUFFER, name="Face_NORMAL")
    face_joint_values = [[skin_joint_indices.get(value, 0) for value in row] for row in face_primitive.joints]
    face_joints = builder.add_accessor(face_joint_values, UNSIGNED_SHORT, "VEC4", ARRAY_BUFFER, name="Face_JOINTS_0")
    face_weights = builder.add_accessor(face_primitive.weights, FLOAT, "VEC4", ARRAY_BUFFER, name="Face_WEIGHTS_0")
    face_indices = builder.add_accessor(face_primitive.indices, UNSIGNED_SHORT, "SCALAR", ELEMENT_ARRAY_BUFFER, name="Face_INDICES")
    morph_accessors = [builder.add_accessor(deltas, FLOAT, "VEC3", ARRAY_BUFFER, name=f"Face_MORPH_{name}") for name, deltas in zip(target_names, target_arrays)]
    face_mesh = builder.add_mesh({
        "name": "Babak_Face_Blendshapes",
        "weights": [0.0] * len(target_names),
        "extras": {"targetNames": target_names, "facial_system": "prototype blendshape channels"},
        "primitives": [{
            "attributes": {"POSITION": face_position, "NORMAL": face_normal, "JOINTS_0": face_joints, "WEIGHTS_0": face_weights},
            "indices": face_indices,
            "material": material_ids["skin"],
            "targets": [{"POSITION": accessor} for accessor in morph_accessors],
        }],
    })
    face_node = builder.add_node({"name": "Face_Blendshapes", "mesh": face_mesh, "skin": 0, "weights": [0.0] * len(target_names), "extras": {"blendShapes": target_names}})
    builder.gltf["nodes"][root]["children"].append(face_node)

    # Skin inverse bind matrices. All rest-pose joints are translation-only.
    inverse_bind = []
    for name in bones:
        inverse_bind.append(mat4_translation(v_mul(positions[name], -1.0)))
    inverse_accessor = builder.add_accessor(inverse_bind, FLOAT, "MAT4", name="Humanoid_InverseBindMatrices", minmax=False)
    skin_index = len(builder.gltf["skins"])
    builder.gltf["skins"].append({
        "name": "Babak_Humanoid_Skin",
        "joints": list(bones.values()),
        "inverseBindMatrices": inverse_accessor,
        "skeleton": bones["Hips"],
        "extras": {"skeleton_type": "humanoid", "ik_ready": True},
    })
    # The mesh nodes were created before the skin index existed; keep their explicit skin ref correct.
    builder.gltf["nodes"][body_node]["skin"] = skin_index
    builder.gltf["nodes"][face_node]["skin"] = skin_index

    # Interaction props are parented to hand bones, so they follow arm animation.
    mug_primitive = StaticPrimitive(material_ids["coffee"])
    add_cylinder(mug_primitive, [0.0, 0.0, 0.0], 0.045, 0.095, material_ids["coffee"])
    add_box(mug_primitive, [0.055, 0.0, 0.0], [0.045, 0.055, 0.018])
    mug_mesh = make_static_mesh(builder, [mug_primitive], "Coffee_Mug")
    mug_node = builder.add_node({"name": "Coffee_Mug", "mesh": mug_mesh, "translation": [0.0, -0.09, 0.12], "extras": {"interaction": "drink_coffee"}})
    builder.gltf["nodes"][bones["RightHand"]]["children"].append(mug_node)

    document_primitive = StaticPrimitive(material_ids["paper"])
    add_box(document_primitive, [0.0, 0.0, 0.0], [0.20, 0.012, 0.27])
    document_mesh = make_static_mesh(builder, [document_primitive], "Document_Paper")
    document_node = builder.add_node({"name": "Document_Paper", "mesh": document_mesh, "translation": [0.0, -0.055, 0.12], "extras": {"interaction": "read_document"}})
    builder.gltf["nodes"][bones["LeftHand"]]["children"].append(document_node)

    # Animation clips. Local bone rotations leave all other joints at the rest pose.
    t_idle = [0.0, 1.0, 2.0]
    add_animation(builder, "idle", 2.0, [
        {"node": bones["Hips"], "path": "translation", "times": t_idle, "values": [[0, 0, 0], [0, 0.008, 0], [0, 0, 0]]},
        {"node": bones["Chest"], "path": "rotation", "times": t_idle, "values": [quat_euler(0, 0, -1.5), quat_euler(0, 0, 1.5), quat_euler(0, 0, -1.5)]},
        {"node": bones["Head"], "path": "rotation", "times": t_idle, "values": [quat_euler(0, -2, 0), quat_euler(0, 2, 0), quat_euler(0, -2, 0)]},
    ], loop=True, description="Subtle breathing and executive idle posture")

    t_walk = [0.0, 0.3, 0.6, 0.9, 1.2]
    add_animation(builder, "walk", 1.2, [
        {"node": bones["Hips"], "path": "translation", "times": t_walk, "values": [[0, 0, 0], [0, 0.025, 0], [0, 0, 0], [0, 0.025, 0], [0, 0, 0]]},
        {"node": bones["LeftUpperLeg"], "path": "rotation", "times": t_walk, "values": [quat_euler(24), quat_euler(-24), quat_euler(24), quat_euler(-24), quat_euler(24)]},
        {"node": bones["RightUpperLeg"], "path": "rotation", "times": t_walk, "values": [quat_euler(-24), quat_euler(24), quat_euler(-24), quat_euler(24), quat_euler(-24)]},
        {"node": bones["LeftLowerLeg"], "path": "rotation", "times": t_walk, "values": [quat_euler(12), quat_euler(0), quat_euler(12), quat_euler(0), quat_euler(12)]},
        {"node": bones["RightLowerLeg"], "path": "rotation", "times": t_walk, "values": [quat_euler(0), quat_euler(12), quat_euler(0), quat_euler(12), quat_euler(0)]},
        {"node": bones["LeftUpperArm"], "path": "rotation", "times": t_walk, "values": [quat_euler(-16), quat_euler(16), quat_euler(-16), quat_euler(16), quat_euler(-16)]},
        {"node": bones["RightUpperArm"], "path": "rotation", "times": t_walk, "values": [quat_euler(16), quat_euler(-16), quat_euler(16), quat_euler(-16), quat_euler(16)]},
    ], loop=True, description="Looping human locomotion cycle")

    sit_values = {
        "Hips": ([0, 0, 0], [0, -0.10, -0.08], [0, -0.12, -0.10]),
        "LeftUpperLeg": (identity_quat(), quat_euler(-60), quat_euler(-60)),
        "RightUpperLeg": (identity_quat(), quat_euler(-60), quat_euler(-60)),
        "LeftLowerLeg": (identity_quat(), quat_euler(70), quat_euler(70)),
        "RightLowerLeg": (identity_quat(), quat_euler(70), quat_euler(70)),
        "LeftFoot": (identity_quat(), quat_euler(-10), quat_euler(-10)),
        "RightFoot": (identity_quat(), quat_euler(-10), quat_euler(-10)),
        "Chest": (identity_quat(), quat_euler(-8), quat_euler(-8)),
    }
    t_sit = [0.0, 0.8, 1.6]
    sit_channels = []
    for bone_name, values in sit_values.items():
        path = "translation" if bone_name == "Hips" else "rotation"
        sit_channels.append({"node": bones[bone_name], "path": path, "times": t_sit, "values": values})
    add_animation(builder, "sit", 1.6, sit_channels, description="Controlled sit-down into an executive chair pose")

    stand_channels = []
    for bone_name, values in sit_values.items():
        path = "translation" if bone_name == "Hips" else "rotation"
        stand_channels.append({"node": bones[bone_name], "path": path, "times": [0.0, 0.8, 1.6], "values": [values[2], values[1], values[0]]})
    add_animation(builder, "stand", 1.6, stand_channels, description="Rise from seated pose to neutral standing")

    t_look = [0.0, 0.5, 1.0, 1.5, 2.0]
    add_animation(builder, "look_at", 2.0, [
        {"node": bones["Neck"], "path": "rotation", "times": t_look, "values": [quat_euler(0, 0, 0), quat_euler(0, 10, 0), quat_euler(0, -12, 0), quat_euler(0, 7, 0), quat_euler(0, 0, 0)]},
        {"node": bones["Head"], "path": "rotation", "times": t_look, "values": [quat_euler(0, 0, 0), quat_euler(0, 18, 0), quat_euler(0, -24, 0), quat_euler(0, 14, 0), quat_euler(0, 0, 0)]},
        {"node": bones["LeftEye"], "path": "rotation", "times": t_look, "values": [quat_euler(0, 0, 0), quat_euler(0, 9, 0), quat_euler(0, -12, 0), quat_euler(0, 7, 0), quat_euler(0, 0, 0)]},
        {"node": bones["RightEye"], "path": "rotation", "times": t_look, "values": [quat_euler(0, 0, 0), quat_euler(0, 9, 0), quat_euler(0, -12, 0), quat_euler(0, 7, 0), quat_euler(0, 0, 0)]},
    ], description="Head, neck and eye target-tracking preview; runtime IK/look-at can override it")

    t_talk = [0.0, 0.25, 0.5, 0.75, 1.0]
    add_animation(builder, "talk", 1.0, [
        {"node": bones["Jaw"], "path": "rotation", "times": t_talk, "values": [quat_euler(0), quat_euler(-12), quat_euler(0), quat_euler(-16), quat_euler(0)]},
        {"node": face_node, "path": "weights", "times": t_talk, "values": [[0, 0, 0, 0], [0.45, 0.05, 0.05, 0.04], [0.12, 0.16, 0, 0], [0.52, 0.02, 0.03, 0.05], [0, 0, 0, 0]]},
        {"node": bones["Head"], "path": "rotation", "times": t_talk, "values": [quat_euler(0, -1, 0), quat_euler(0, 2, 0), quat_euler(0, -2, 0), quat_euler(0, 1, 0), quat_euler(0, -1, 0)]},
    ], loop=True, description="Jaw and facial blendshape speech preview")

    add_animation(builder, "listen", 1.6, [
        {"node": bones["Head"], "path": "rotation", "times": [0, 0.8, 1.6], "values": [quat_euler(0, 0, 0), quat_euler(2, -5, -3), quat_euler(0, 0, 0)]},
        {"node": bones["Chest"], "path": "rotation", "times": [0, 0.8, 1.6], "values": [quat_euler(0), quat_euler(0, 0, 1), quat_euler(0)]},
    ], description="Attentive listening posture")

    add_animation(builder, "wave", 1.8, [
        {"node": bones["RightUpperArm"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5, 1.8], "values": [quat_euler(0), quat_euler(0, 0, 78), quat_euler(0, 0, 92), quat_euler(0, 0, 78), quat_euler(0)]},
        {"node": bones["RightLowerArm"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5, 1.8], "values": [quat_euler(0), quat_euler(0, 0, -22), quat_euler(0, 0, 18), quat_euler(0, 0, -22), quat_euler(0)]},
        {"node": bones["RightHand"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5, 1.8], "values": [quat_euler(0), quat_euler(0, -10, 0), quat_euler(0, 12, 0), quat_euler(0, -10, 0), quat_euler(0)]},
    ], description="Friendly executive wave")

    add_animation(builder, "drink_coffee", 2.4, [
        {"node": bones["RightUpperArm"], "path": "rotation", "times": [0, 0.6, 1.2, 1.8, 2.4], "values": [quat_euler(0), quat_euler(0, 0, 66), quat_euler(0, 0, 84), quat_euler(0, 0, 66), quat_euler(0)]},
        {"node": bones["RightLowerArm"], "path": "rotation", "times": [0, 0.6, 1.2, 1.8, 2.4], "values": [quat_euler(0), quat_euler(0, 0, -22), quat_euler(0, 0, -42), quat_euler(0, 0, -22), quat_euler(0)]},
        {"node": bones["Head"], "path": "rotation", "times": [0, 0.6, 1.2, 1.8, 2.4], "values": [quat_euler(0), quat_euler(5, 0, 0), quat_euler(12, 0, 0), quat_euler(5, 0, 0), quat_euler(0)]},
        {"node": face_node, "path": "weights", "times": [0, 0.6, 1.2, 1.8, 2.4], "values": [[0, 0, 0, 0], [0, 0.03, 0, 0], [0, 0.02, 0, 0], [0, 0.03, 0, 0], [0, 0, 0, 0]]},
    ], description="Right-hand mug interaction with head and face response")

    add_animation(builder, "point", 1.5, [
        {"node": bones["RightUpperArm"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5], "values": [quat_euler(0), quat_euler(0, 0, 72), quat_euler(0, 0, 76), quat_euler(0)]},
        {"node": bones["RightLowerArm"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5], "values": [quat_euler(0), quat_euler(0, 0, -12), quat_euler(0, 0, -8), quat_euler(0)]},
        {"node": bones["Head"], "path": "rotation", "times": [0, 0.5, 1.0, 1.5], "values": [quat_euler(0), quat_euler(0, 8, 0), quat_euler(0, 8, 0), quat_euler(0)]},
    ], description="Directional pointing gesture")

    add_animation(builder, "read_document", 2.0, [
        {"node": bones["LeftUpperArm"], "path": "rotation", "times": [0, 0.7, 1.4, 2.0], "values": [quat_euler(0), quat_euler(0, 0, -48), quat_euler(0, 0, -48), quat_euler(0)]},
        {"node": bones["RightUpperArm"], "path": "rotation", "times": [0, 0.7, 1.4, 2.0], "values": [quat_euler(0), quat_euler(0, 0, 48), quat_euler(0, 0, 48), quat_euler(0)]},
        {"node": bones["Head"], "path": "rotation", "times": [0, 0.7, 1.4, 2.0], "values": [quat_euler(0), quat_euler(17, 0, 0), quat_euler(17, 0, 0), quat_euler(0)]},
    ], description="Two-hand document reading posture")

    add_animation(builder, "move_between_departments", 4.0, [
        {"node": root, "path": "translation", "times": [0, 1.3, 2.6, 4.0], "values": [[0, 0, 0], [0.65, 0, 0], [1.35, 0, 0.35], [2.0, 0, 0.75]]},
        {"node": root, "path": "rotation", "times": [0, 1.3, 2.6, 4.0], "values": [quat_euler(0, 0, 0), quat_euler(0, 12, 0), quat_euler(0, 32, 0), quat_euler(0, 48, 0)]},
    ], description="Root motion between mapped company departments")

    builder.gltf["extras"] = {
        "character_id": "BAC-0001",
        "name": "Babak Moradvand",
        "role": "Chief Executive Officer",
        "height_cm": 188,
        "asset_status": "rigged-glb-prototype",
        "visual_reference": "../babak-moradvand-3d-concept.png",
        "personnel_photo": "../babak-moradvand-personnel-photo.webp",
        "ik": {
            "method": "runtime FABRIK/CCD solver",
            "chains": {
                "leftArm": ["LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand"],
                "rightArm": ["RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand"],
                "leftLeg": ["Hips", "LeftUpperLeg", "LeftLowerLeg", "LeftFoot"],
                "rightLeg": ["Hips", "RightUpperLeg", "RightLowerLeg", "RightFoot"],
            },
        },
        "look_at": {"head": "Head", "neck": "Neck", "eye_bones": ["LeftEye", "RightEye"], "target_space": "world"},
        "blend_shapes": ["mouthOpen", "smile", "blinkLeft", "blinkRight"],
        "interaction_props": {"coffee": "Coffee_Mug", "document": "Document_Paper"},
        "runtime": "../babak-moradvand-rig-runtime.js",
        "animation_names": [animation["name"] for animation in builder.gltf["animations"]],
        "vrm": {"status": "export-pending", "target": "VRM 1.0 humanoid"},
        "production_note": "This dependency-free GLB is a technical blocking asset. Replace its mannequin geometry with the final likeness/PBR model before public production use.",
    }

    # Mark the mesh nodes with the final skin index after all resources exist.
    builder.gltf["nodes"][body_node]["skin"] = skin_index
    builder.gltf["nodes"][face_node]["skin"] = skin_index
    builder.finish(OUT)

    manifest = {
        "character_id": "BAC-0001",
        "name": "Babak Moradvand",
        "role": "Chief Executive Officer",
        "height_cm": 188,
        "asset": "babak-moradvand-rigged.glb",
        "runtime": "babak-moradvand-rig-runtime.js",
        "asset_type": "rigged-glb-prototype",
        "status": "prototype-rigged",
        "vrm_status": "export-pending",
        "generated_without_install": True,
        "skeleton": [
            {"name": name, "parent": bone_parents[name], "humanoid": builder.gltf["nodes"][bones[name]]["extras"]["humanoidBone"]}
            for name in bones
        ],
        "ik_chains": {
            "left_arm": ["LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand"],
            "right_arm": ["RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand"],
            "left_leg": ["Hips", "LeftUpperLeg", "LeftLowerLeg", "LeftFoot"],
            "right_leg": ["Hips", "RightUpperLeg", "RightLowerLeg", "RightFoot"],
        },
        "look_at": {"neck_bone": "Neck", "head_bone": "Head", "target_space": "world", "runtime_solver": "yaw-pitch clamp"},
        "blend_shapes": ["mouthOpen", "smile", "blinkLeft", "blinkRight"],
        "actions": [
            {"name": animation["name"], "duration_seconds": animation["extras"]["duration_seconds"], "loop": animation["extras"]["loop"], "description": animation["extras"]["description"]}
            for animation in builder.gltf["animations"]
        ],
        "interaction_nodes": {"coffee": "Coffee_Mug", "document": "Document_Paper"},
        "reference_assets": {
            "concept": "../babak-moradvand-3d-concept.png",
            "personnel_photo": "../babak-moradvand-personnel-photo.webp",
        },
        "next_production_step": "Import the GLB into Blender/Unity/Unreal, replace blocking geometry with the final likeness, validate humanoid mapping, then export VRM 1.0.",
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"glb": str(OUT), "bytes": OUT.stat().st_size, "animations": len(builder.gltf["animations"]), "bones": len(bones), "blend_shapes": len(target_names)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
