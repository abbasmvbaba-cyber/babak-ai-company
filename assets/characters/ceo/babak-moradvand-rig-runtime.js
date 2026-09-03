/*
 * Babak Moradvand · CEO rig runtime contract
 *
 * Dependency-free animation/IK helpers. The GLB contains the skeleton and baked
 * preview clips; this module supplies the runtime layer that a Three.js, Babylon,
 * Unity or custom WebGL adapter can connect to without changing the asset.
 */

export const BABAK_CEO_RIG = Object.freeze({
  characterId: 'BAC-0001',
  heightCm: 188,
  model: 'babak-moradvand-rigged.glb',
  bones: Object.freeze({
    hips: 'Hips', spine: 'Spine', chest: 'Chest', neck: 'Neck', head: 'Head', jaw: 'Jaw',
    leftEye: 'LeftEye', rightEye: 'RightEye',
    leftShoulder: 'LeftShoulder', leftUpperArm: 'LeftUpperArm', leftLowerArm: 'LeftLowerArm', leftHand: 'LeftHand',
    rightShoulder: 'RightShoulder', rightUpperArm: 'RightUpperArm', rightLowerArm: 'RightLowerArm', rightHand: 'RightHand',
    leftUpperLeg: 'LeftUpperLeg', leftLowerLeg: 'LeftLowerLeg', leftFoot: 'LeftFoot',
    rightUpperLeg: 'RightUpperLeg', rightLowerLeg: 'RightLowerLeg', rightFoot: 'RightFoot',
  }),
  ikChains: Object.freeze({
    leftArm: Object.freeze(['LeftShoulder', 'LeftUpperArm', 'LeftLowerArm', 'LeftHand']),
    rightArm: Object.freeze(['RightShoulder', 'RightUpperArm', 'RightLowerArm', 'RightHand']),
    leftLeg: Object.freeze(['Hips', 'LeftUpperLeg', 'LeftLowerLeg', 'LeftFoot']),
    rightLeg: Object.freeze(['Hips', 'RightUpperLeg', 'RightLowerLeg', 'RightFoot']),
  }),
  blendShapes: Object.freeze(['mouthOpen', 'smile', 'blinkLeft', 'blinkRight']),
  actions: Object.freeze([
    'idle', 'walk', 'sit', 'stand', 'look_at', 'talk', 'listen', 'wave',
    'drink_coffee', 'point', 'read_document', 'move_between_departments',
  ]),
});

const EPSILON = 1e-6;

const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const scale = (a, amount) => [a[0] * amount, a[1] * amount, a[2] * amount];
const length = (a) => Math.hypot(a[0], a[1], a[2]);
const distance = (a, b) => length(sub(a, b));
const normalize = (a) => {
  const size = length(a);
  return size < EPSILON ? [0, 0, 0] : scale(a, 1 / size);
};
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

/**
 * Solve a positional IK chain using FABRIK.
 *
 * @param {Array<[number,number,number]>} inputPoints - root to end-effector points.
 * @param {[number,number,number]} target - desired end-effector world position.
 * @param {object} options - lengths, iterations, tolerance and optional root lock.
 * @returns {{points: Array<[number,number,number]>, reached: boolean, distance: number}}
 */
export function solveFabrik(inputPoints, target, options = {}) {
  if (!Array.isArray(inputPoints) || inputPoints.length < 2) {
    throw new Error('FABRIK requires at least two points');
  }
  const points = inputPoints.map((point) => [...point]);
  const root = [...points[0]];
  const lengths = options.lengths || points.slice(0, -1).map((point, index) => distance(point, points[index + 1]));
  const totalLength = lengths.reduce((sum, value) => sum + value, 0);
  const tolerance = options.tolerance ?? 0.001;
  const iterations = options.iterations ?? 10;
  const targetDistance = distance(root, target);

  if (targetDistance >= totalLength - EPSILON) {
    const direction = normalize(sub(target, root));
    points[0] = root;
    for (let index = 0; index < lengths.length; index += 1) {
      points[index + 1] = add(points[index], scale(direction, lengths[index]));
    }
    return { points, reached: false, distance: distance(points[points.length - 1], target) };
  }

  for (let iteration = 0; iteration < iterations; iteration += 1) {
    points[points.length - 1] = [...target];
    for (let index = points.length - 2; index >= 0; index -= 1) {
      const direction = normalize(sub(points[index], points[index + 1]));
      points[index] = add(points[index + 1], scale(direction, lengths[index]));
    }
    points[0] = [...root];
    for (let index = 0; index < points.length - 1; index += 1) {
      const direction = normalize(sub(points[index + 1], points[index]));
      points[index + 1] = add(points[index], scale(direction, lengths[index]));
    }
    if (distance(points[points.length - 1], target) <= tolerance) break;
  }

  const endDistance = distance(points[points.length - 1], target);
  return { points, reached: endDistance <= tolerance, distance: endDistance };
}

/**
 * Calculate clamped yaw/pitch for a head and eye target. The GLB faces +Z.
 */
export function solveLookAt(headPosition, target, options = {}) {
  const direction = sub(target, headPosition);
  const horizontal = Math.hypot(direction[0], direction[2]);
  const yaw = Math.atan2(direction[0], direction[2]) * 180 / Math.PI;
  const pitch = Math.atan2(direction[1], Math.max(horizontal, EPSILON)) * 180 / Math.PI;
  return {
    yaw: clamp(yaw, options.minYaw ?? -55, options.maxYaw ?? 55),
    pitch: clamp(pitch, options.minPitch ?? -30, options.maxPitch ?? 30),
  };
}

export function speechWeights({ mouthOpen = 0, smile = 0, blinkLeft = 0, blinkRight = 0 } = {}) {
  return {
    mouthOpen: clamp(mouthOpen, 0, 1),
    smile: clamp(smile, 0, 1),
    blinkLeft: clamp(blinkLeft, 0, 1),
    blinkRight: clamp(blinkRight, 0, 1),
  };
}

/**
 * A small adapter-oriented controller. The adapter is deliberately tiny:
 * playAnimation(name, options), setBoneEuler(name, eulerDegrees),
 * setBonePosition(name, position), setBlendShape(name, weight).
 */
export function createCharacterController(adapter) {
  if (!adapter) throw new Error('A character adapter is required');
  let activeAction = 'idle';

  const play = (name, options = {}) => {
    if (!BABAK_CEO_RIG.actions.includes(name)) throw new Error(`Unknown CEO action: ${name}`);
    activeAction = name;
    adapter.playAnimation?.(name, { loop: name === 'idle' || name === 'walk' || name === 'talk', ...options });
    return activeAction;
  };

  const lookAt = (headPosition, target, options = {}) => {
    const rotation = solveLookAt(headPosition, target, options);
    adapter.setBoneEuler?.('Neck', [rotation.pitch * 0.35, rotation.yaw * 0.35, 0]);
    adapter.setBoneEuler?.('Head', [rotation.pitch * 0.65, rotation.yaw * 0.65, 0]);
    adapter.setBoneEuler?.('LeftEye', [rotation.pitch * 0.15, rotation.yaw * 0.20, 0]);
    adapter.setBoneEuler?.('RightEye', [rotation.pitch * 0.15, rotation.yaw * 0.20, 0]);
    return rotation;
  };

  const setSpeech = (weights) => {
    const normalized = speechWeights(weights);
    Object.entries(normalized).forEach(([name, weight]) => adapter.setBlendShape?.(name, weight));
    return normalized;
  };

  const solveArm = (side, points, target, options = {}) => {
    const result = solveFabrik(points, target, options);
    const chain = side === 'left' ? BABAK_CEO_RIG.ikChains.leftArm : BABAK_CEO_RIG.ikChains.rightArm;
    result.points.forEach((position, index) => adapter.setBonePosition?.(chain[index], position));
    return result;
  };

  return Object.freeze({
    play,
    lookAt,
    setSpeech,
    solveArm,
    get activeAction() { return activeAction; },
  });
}
