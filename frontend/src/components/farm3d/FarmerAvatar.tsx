import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface FarmerAvatarProps {
  isIrrigating: boolean;
  activeZoneId: string;
}

// Walking path waypoints through the crop rows and irrigation valves
const PATH_WAYPOINTS: THREE.Vector3[] = [
  new THREE.Vector3(-4, 0, 3),   // Near farmhouse / tool shed
  new THREE.Vector3(-1, 0, 3),   // Inspection path row 1
  new THREE.Vector3(2, 0, 3),    // Near Zone South-B
  new THREE.Vector3(4, 0, 1),    // Field corner turn
  new THREE.Vector3(4, 0, -2),   // East boundary path
  new THREE.Vector3(1, 0, -3),   // North-East irrigation manifold
  new THREE.Vector3(-2, 0, -3),  // Near Zone North-A (Main Valve)
  new THREE.Vector3(-4, 0, -1),  // West perimeter fence
];

export const FarmerAvatar: React.FC<FarmerAvatarProps> = ({ isIrrigating }) => {
  const farmerGroupRef = useRef<THREE.Group>(null);
  const leftLegRef = useRef<THREE.Mesh>(null);
  const rightLegRef = useRef<THREE.Mesh>(null);
  const leftArmRef = useRef<THREE.Mesh>(null);
  const rightArmRef = useRef<THREE.Mesh>(null);
  const headRef = useRef<THREE.Group>(null);

  // Animation state tracking
  const stateRef = useRef({
    currentWaypointIndex: 0,
    progress: 0,
    speed: 0.008,
    isInspecting: false,
    inspectTimer: 0,
    walkCycle: 0,
  });

  useFrame((_, delta) => {
    if (!farmerGroupRef.current) return;

    const state = stateRef.current;

    // If irrigation is active and farmer is near the main valve waypoint (index 6), pause to inspect
    if (isIrrigating && state.currentWaypointIndex === 6 && !state.isInspecting) {
      state.isInspecting = true;
      state.inspectTimer = 4.0; // inspect for 4 seconds
    }

    if (state.isInspecting) {
      state.inspectTimer -= delta;
      // Head nodding / examining pipes
      if (headRef.current) {
        headRef.current.rotation.x = Math.sin(Date.now() * 0.005) * 0.15 + 0.2;
      }
      // Reset limbs to standing position
      if (leftLegRef.current) leftLegRef.current.rotation.x = 0;
      if (rightLegRef.current) rightLegRef.current.rotation.x = 0;
      if (leftArmRef.current) leftArmRef.current.rotation.x = 0.3;
      if (rightArmRef.current) rightArmRef.current.rotation.x = -0.3;

      if (state.inspectTimer <= 0) {
        state.isInspecting = false;
      }
      return;
    }

    // Walking movement along waypoints
    const startPt = PATH_WAYPOINTS[state.currentWaypointIndex];
    const nextIndex = (state.currentWaypointIndex + 1) % PATH_WAYPOINTS.length;
    const endPt = PATH_WAYPOINTS[nextIndex];

    state.progress += state.speed;
    if (state.progress >= 1.0) {
      state.progress = 0;
      state.currentWaypointIndex = nextIndex;
    }

    // Interpolate position
    farmerGroupRef.current.position.lerpVectors(startPt, endPt, state.progress);

    // Compute direction vector and rotate smoothly towards it
    const direction = new THREE.Vector3().subVectors(endPt, startPt).normalize();
    const targetAngle = Math.atan2(direction.x, direction.z);
    
    // Smooth rotation interpolation
    let currentAngle = farmerGroupRef.current.rotation.y;
    // Normalize angle difference to avoid 360 wrap
    let diff = targetAngle - currentAngle;
    while (diff < -Math.PI) diff += Math.PI * 2;
    while (diff > Math.PI) diff -= Math.PI * 2;
    farmerGroupRef.current.rotation.y += diff * 0.1;

    // Limb swing walking animation
    state.walkCycle += delta * 7.5; // Walk cadence
    const swingAngle = Math.sin(state.walkCycle) * 0.45;

    if (leftLegRef.current) leftLegRef.current.rotation.x = swingAngle;
    if (rightLegRef.current) rightLegRef.current.rotation.x = -swingAngle;
    if (leftArmRef.current) leftArmRef.current.rotation.x = -swingAngle * 0.7;
    if (rightArmRef.current) rightArmRef.current.rotation.x = swingAngle * 0.7;

    // Subtle torso bobbing
    farmerGroupRef.current.position.y = Math.abs(Math.sin(state.walkCycle * 2)) * 0.05;
  });

  return (
    <group ref={farmerGroupRef} position={[-4, 0, 3]}>
      {/* Shadow disc */}
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.3, 16]} />
        <meshBasicMaterial color="#000000" opacity={0.35} transparent />
      </mesh>

      {/* --- LEGS --- */}
      {/* Left Leg */}
      <group position={[-0.1, 0.45, 0]}>
        <mesh ref={leftLegRef} position={[0, -0.22, 0]} castShadow>
          <boxGeometry args={[0.12, 0.45, 0.12]} />
          <meshStandardMaterial color="#1e3a8a" roughness={0.7} /> {/* Blue denim */}
          {/* Boot */}
          <mesh position={[0, -0.22, 0.03]}>
            <boxGeometry args={[0.13, 0.1, 0.18]} />
            <meshStandardMaterial color="#451a03" roughness={0.9} /> {/* Brown leather */}
          </mesh>
        </mesh>
      </group>

      {/* Right Leg */}
      <group position={[0.1, 0.45, 0]}>
        <mesh ref={rightLegRef} position={[0, -0.22, 0]} castShadow>
          <boxGeometry args={[0.12, 0.45, 0.12]} />
          <meshStandardMaterial color="#1e3a8a" roughness={0.7} />
          {/* Boot */}
          <mesh position={[0, -0.22, 0.03]}>
            <boxGeometry args={[0.13, 0.1, 0.18]} />
            <meshStandardMaterial color="#451a03" roughness={0.9} />
          </mesh>
        </mesh>
      </group>

      {/* --- TORSO & SHIRT --- */}
      <mesh position={[0, 0.72, 0]} castShadow>
        <boxGeometry args={[0.32, 0.42, 0.2]} />
        <meshStandardMaterial color="#dc2626" roughness={0.6} /> {/* Red checkered work shirt */}
      </mesh>

      {/* Belt */}
      <mesh position={[0, 0.52, 0]}>
        <boxGeometry args={[0.33, 0.06, 0.21]} />
        <meshStandardMaterial color="#1f2937" roughness={0.8} />
      </mesh>

      {/* --- ARMS --- */}
      {/* Left Arm */}
      <group position={[-0.22, 0.88, 0]}>
        <mesh ref={leftArmRef} position={[0, -0.18, 0]} castShadow>
          <boxGeometry args={[0.1, 0.36, 0.1]} />
          <meshStandardMaterial color="#dc2626" roughness={0.6} />
          {/* Hand */}
          <mesh position={[0, -0.19, 0]}>
            <sphereGeometry args={[0.05, 8, 8]} />
            <meshStandardMaterial color="#fcd34d" roughness={0.5} />
          </mesh>
        </mesh>
      </group>

      {/* Right Arm */}
      <group position={[0.22, 0.88, 0]}>
        <mesh ref={rightArmRef} position={[0, -0.18, 0]} castShadow>
          <boxGeometry args={[0.1, 0.36, 0.1]} />
          <meshStandardMaterial color="#dc2626" roughness={0.6} />
          {/* Hand */}
          <mesh position={[0, -0.19, 0]}>
            <sphereGeometry args={[0.05, 8, 8]} />
            <meshStandardMaterial color="#fcd34d" roughness={0.5} />
          </mesh>
        </mesh>
      </group>

      {/* --- HEAD & STRAW HAT --- */}
      <group ref={headRef} position={[0, 1.05, 0]}>
        {/* Head */}
        <mesh castShadow>
          <boxGeometry args={[0.2, 0.22, 0.2]} />
          <meshStandardMaterial color="#fcd34d" roughness={0.5} />
        </mesh>

        {/* Straw Hat Brim */}
        <mesh position={[0, 0.11, 0]} rotation={[0.05, 0, 0]}>
          <cylinderGeometry args={[0.32, 0.32, 0.03, 16]} />
          <meshStandardMaterial color="#ca8a04" roughness={0.9} /> {/* Golden straw */}
        </mesh>

        {/* Straw Hat Crown */}
        <mesh position={[0, 0.2, 0]} rotation={[0.05, 0, 0]}>
          <cylinderGeometry args={[0.18, 0.2, 0.16, 16]} />
          <meshStandardMaterial color="#b45309" roughness={0.9} />
        </mesh>

        {/* Hat Ribbon */}
        <mesh position={[0, 0.15, 0]} rotation={[0.05, 0, 0]}>
          <cylinderGeometry args={[0.205, 0.205, 0.04, 16]} />
          <meshStandardMaterial color="#1e293b" />
        </mesh>
      </group>

      {/* Name tag floating above farmer */}
      <group position={[0, 1.45, 0]}>
        {/* Simple visual indicator beacon */}
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[0.04, 8, 8]} />
          <meshBasicMaterial color="#34d399" />
        </mesh>
      </group>
    </group>
  );
};
