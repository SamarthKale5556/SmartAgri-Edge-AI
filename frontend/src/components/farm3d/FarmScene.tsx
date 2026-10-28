import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Center } from '@react-three/drei';
import * as THREE from 'three';
import { FarmerAvatar } from './FarmerAvatar';
import { useFarm } from '../../context/FarmContext';
import { RotateCcw, Droplets } from 'lucide-react';

interface FieldSectorProps {
  id: string;
  position: [number, number, number];
  size: [number, number];
  name: string;
  moisture: number;
  isSelected: boolean;
  isIrrigating: boolean;
  onSelect: (id: string) => void;
}

// Interactive Field Sector
const FieldSector: React.FC<FieldSectorProps> = ({
  id,
  position,
  size,
  moisture,
  isSelected,
  isIrrigating,
  onSelect,
}) => {
  const [hovered, setHovered] = useState(false);

  // Dynamic soil color based on moisture level:
  const soilColor = moisture < 22 ? '#8c6d48' : moisture < 38 ? '#523a28' : '#2b1d14';

  return (
    <group position={position}>
      {/* Clickable Soil Bed */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        receiveShadow
        onClick={(e) => {
          e.stopPropagation();
          onSelect(id);
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          setHovered(true);
        }}
        onPointerOut={() => setHovered(false)}
      >
        <planeGeometry args={[size[0], size[1], 8, 8]} />
        <meshStandardMaterial
          color={soilColor}
          roughness={0.9}
          metalness={0.05}
        />
      </mesh>

      {/* Raised Furrow Ridges */}
      {[-1.8, -0.9, 0, 0.9, 1.8].map((offset, i) => (
        <mesh key={i} position={[offset, 0.04, 0]} receiveShadow>
          <boxGeometry args={[0.35, 0.08, size[1] - 0.2]} />
          <meshStandardMaterial color={soilColor} roughness={0.95} />
        </mesh>
      ))}

      {/* Crop Stalks arranged in rows */}
      {[-1.8, -0.9, 0, 0.9, 1.8].map((rowX, rIdx) =>
        [-2.0, -1.2, -0.4, 0.4, 1.2, 2.0].map((cropZ, cIdx) => {
          const plantHeight = 0.5 + ((rIdx + cIdx) % 3) * 0.12;
          const leafColor = moisture < 20 ? '#a39744' : '#22c55e';
          return (
            <group key={`${rIdx}-${cIdx}`} position={[rowX, 0.08, cropZ]}>
              <mesh position={[0, plantHeight / 2, 0]} castShadow>
                <cylinderGeometry args={[0.025, 0.04, plantHeight, 6]} />
                <meshStandardMaterial color="#166534" roughness={0.7} />
              </mesh>
              <mesh position={[0, plantHeight * 0.7, 0]} castShadow>
                <coneGeometry args={[0.18, 0.35, 5]} />
                <meshStandardMaterial color={leafColor} roughness={0.6} />
              </mesh>
              <mesh position={[0, plantHeight + 0.05, 0]}>
                <sphereGeometry args={[0.04, 6, 6]} />
                <meshStandardMaterial color="#eab308" />
              </mesh>
            </group>
          );
        })
      )}

      {/* Active Irrigation Water Spray Effect */}
      {isIrrigating && isSelected && (
        <group position={[0, 0.3, 0]}>
          {[-1.5, 0, 1.5].map((sprinklerX, sIdx) => (
            <group key={sIdx} position={[sprinklerX, 0, 0]}>
              <mesh position={[0, 0.2, 0]}>
                <sphereGeometry args={[0.08, 8, 8]} />
                <meshStandardMaterial color="#38bdf8" emissive="#0284c7" emissiveIntensity={0.8} />
              </mesh>
              <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.1, 0]}>
                <ringGeometry args={[0.4, 1.2, 16]} />
                <meshBasicMaterial color="#7dd3fc" transparent opacity={0.45} side={THREE.DoubleSide} />
              </mesh>
            </group>
          ))}
        </group>
      )}

      {/* Glowing Selection / Hover Outline */}
      {(isSelected || hovered) && (
        <lineSegments position={[0, 0.05, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <edgesGeometry args={[new THREE.PlaneGeometry(size[0] + 0.1, size[1] + 0.1)]} />
          <lineBasicMaterial color={isSelected ? '#34d399' : '#fbbf24'} linewidth={2} />
        </lineSegments>
      )}

      {/* Floating Zone Label */}
      <group position={[0, 0.9, -size[1] / 2 + 0.3]}>
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[1.4, 0.28, 0.05]} />
          <meshBasicMaterial color="#0f172a" />
        </mesh>
      </group>
    </group>
  );
};

// Water Tank & Irrigation Pipes
const IrrigationInfrastructure: React.FC<{ isIrrigating: boolean }> = ({ isIrrigating }) => {
  const pipeRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (isIrrigating && pipeRef.current) {
      const mat = pipeRef.current.material as THREE.MeshStandardMaterial;
      mat.emissiveIntensity = 0.5 + Math.sin(Date.now() * 0.008) * 0.4;
    }
  });

  return (
    <group position={[-5, 0, -4]}>
      {/* Tank Wooden Platform Stilts */}
      {[-0.5, 0.5].map((x) =>
        [-0.5, 0.5].map((z, idx) => (
          <mesh key={idx} position={[x, 0.9, z]} castShadow>
            <cylinderGeometry args={[0.08, 0.08, 1.8, 8]} />
            <meshStandardMaterial color="#5c3a21" roughness={0.9} />
          </mesh>
        ))
      )}

      <mesh position={[0, 1.85, 0]} castShadow>
        <boxGeometry args={[1.5, 0.12, 1.5]} />
        <meshStandardMaterial color="#78350f" roughness={0.8} />
      </mesh>

      <mesh position={[0, 2.7, 0]} castShadow>
        <cylinderGeometry args={[0.8, 0.8, 1.6, 20]} />
        <meshStandardMaterial color="#334155" metalness={0.7} roughness={0.3} />
      </mesh>

      <mesh position={[0, 3.55, 0]}>
        <coneGeometry args={[0.85, 0.35, 20]} />
        <meshStandardMaterial color="#1e293b" metalness={0.6} />
      </mesh>

      <mesh ref={pipeRef} position={[2.5, 0.1, 1]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.06, 0.06, 6.5, 12]} />
        <meshStandardMaterial
          color={isIrrigating ? '#0284c7' : '#475569'}
          emissive={isIrrigating ? '#38bdf8' : '#000000'}
          emissiveIntensity={isIrrigating ? 0.7 : 0}
          roughness={0.4}
        />
      </mesh>

      <mesh position={[0.2, 0.25, 0.5]}>
        <boxGeometry args={[0.25, 0.35, 0.25]} />
        <meshStandardMaterial color={isIrrigating ? '#22c55e' : '#ef4444'} roughness={0.5} />
      </mesh>
    </group>
  );
};

const Farmhouse: React.FC = () => {
  return (
    <group position={[-5, 0, 3]} rotation={[0, Math.PI / 4, 0]}>
      <mesh position={[0, 1.0, 0]} castShadow receiveShadow>
        <boxGeometry args={[2.4, 2.0, 1.8]} />
        <meshStandardMaterial color="#b91c1c" roughness={0.8} />
      </mesh>

      <mesh position={[0, 2.45, 0]} rotation={[0, 0, 0]} castShadow>
        <coneGeometry args={[1.8, 1.1, 4]} />
        <meshStandardMaterial color="#451a03" roughness={0.7} />
      </mesh>

      <mesh position={[0, 0.65, 0.91]}>
        <planeGeometry args={[0.8, 1.3]} />
        <meshStandardMaterial color="#1f2937" roughness={0.9} />
      </mesh>

      <mesh position={[0.6, 2.6, 0.3]} castShadow>
        <boxGeometry args={[0.3, 0.9, 0.3]} />
        <meshStandardMaterial color="#78350f" roughness={0.9} />
      </mesh>
    </group>
  );
};

const WaterPond: React.FC = () => {
  return (
    <group position={[5.2, 0.02, 3]}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <circleGeometry args={[1.6, 24]} />
        <meshStandardMaterial color="#0284c7" roughness={0.1} metalness={0.8} />
      </mesh>

      {[0, 45, 90, 135, 180, 225, 270, 315].map((deg, i) => {
        const rad = (deg * Math.PI) / 180;
        const x = Math.cos(rad) * 1.65;
        const z = Math.sin(rad) * 1.65;
        return (
          <mesh key={i} position={[x, 0.08, z]} castShadow>
            <dodecahedronGeometry args={[0.2 + (i % 3) * 0.06]} />
            <meshStandardMaterial color="#64748b" roughness={0.9} />
          </mesh>
        );
      })}
    </group>
  );
};

const Tree: React.FC<{ position: [number, number, number]; scale?: number }> = ({ position, scale = 1 }) => {
  return (
    <group position={position} scale={scale}>
      <mesh position={[0, 0.6, 0]} castShadow>
        <cylinderGeometry args={[0.12, 0.16, 1.2, 6]} />
        <meshStandardMaterial color="#451a03" roughness={0.9} />
      </mesh>
      <mesh position={[0, 1.5, 0]} castShadow>
        <coneGeometry args={[0.8, 1.2, 6]} />
        <meshStandardMaterial color="#15803d" roughness={0.7} />
      </mesh>
      <mesh position={[0, 2.2, 0]} castShadow>
        <coneGeometry args={[0.6, 1.0, 6]} />
        <meshStandardMaterial color="#16a34a" roughness={0.7} />
      </mesh>
    </group>
  );
};

export const FarmScene: React.FC = () => {
  const { fieldZones, activeZoneId, setActiveZoneId, isIrrigating } = useFarm();
  const controlsRef = useRef<any>(null);

  const resetCamera = () => {
    if (controlsRef.current) {
      controlsRef.current.reset();
      controlsRef.current.object.position.set(13, 11, 13);
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
    }
  };

  const activeZone = fieldZones[activeZoneId];

  return (
    <div className="relative w-full h-[520px] rounded-xl overflow-hidden border border-white/10 shadow-2xl bg-gradient-to-b from-[#0b1320] to-[#060a12]">
      <Canvas
        shadows
        camera={{ position: [13, 11, 13], fov: 38 }}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
      >
        <OrbitControls
          ref={controlsRef}
          enableDamping
          dampingFactor={0.06}
          maxPolarAngle={Math.PI / 2.1}
          minDistance={6}
          maxDistance={30}
        />

        <ambientLight intensity={0.4} color="#fef08a" />
        <directionalLight
          position={[12, 18, 8]}
          intensity={1.2}
          color="#fffbeb"
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-far={45}
          shadow-camera-left={-10}
          shadow-camera-right={10}
          shadow-camera-top={10}
          shadow-camera-bottom={-10}
          shadow-bias={-0.0005}
        />
        <hemisphereLight args={['#38bdf8', '#14532d', 0.4]} />

        <Center>
          <group position={[0, 0, 0]}>
            <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.02, 0]} receiveShadow>
              <planeGeometry args={[22, 18]} />
              <meshStandardMaterial color="#14532d" roughness={0.9} />
            </mesh>

            <FieldSector
              id="North-Field-A"
              position={[-2.3, 0, -2.5]}
              size={[4.2, 4.4]}
              name="North-A (Wheat)"
              moisture={fieldZones['North-Field-A']?.soilMoisture ?? 22}
              isSelected={activeZoneId === 'North-Field-A'}
              isIrrigating={isIrrigating}
              onSelect={setActiveZoneId}
            />

            <FieldSector
              id="North-Field-B"
              position={[2.3, 0, -2.5]}
              size={[4.2, 4.4]}
              name="North-B (Corn)"
              moisture={fieldZones['North-Field-B']?.soilMoisture ?? 38}
              isSelected={activeZoneId === 'North-Field-B'}
              isIrrigating={isIrrigating}
              onSelect={setActiveZoneId}
            />

            <FieldSector
              id="South-Field-A"
              position={[-2.3, 0, 2.5]}
              size={[4.2, 4.4]}
              name="South-A (Soy)"
              moisture={fieldZones['South-Field-A']?.soilMoisture ?? 18}
              isSelected={activeZoneId === 'South-Field-A'}
              isIrrigating={isIrrigating}
              onSelect={setActiveZoneId}
            />

            <FieldSector
              id="South-Field-B"
              position={[2.3, 0, 2.5]}
              size={[4.2, 4.4]}
              name="South-B (Barley)"
              moisture={fieldZones['South-Field-B']?.soilMoisture ?? 44}
              isSelected={activeZoneId === 'South-Field-B'}
              isIrrigating={isIrrigating}
              onSelect={setActiveZoneId}
            />

            <Farmhouse />
            <IrrigationInfrastructure isIrrigating={isIrrigating} />
            <WaterPond />

            <FarmerAvatar isIrrigating={isIrrigating} activeZoneId={activeZoneId} />

            <Tree position={[-7.5, 0, -6]} scale={1.2} />
            <Tree position={[-5.5, 0, -6.8]} scale={1.0} />
            <Tree position={[6.5, 0, -5.5]} scale={1.3} />
            <Tree position={[7.8, 0, -3.0]} scale={0.9} />
            <Tree position={[7.5, 0, 5.5]} scale={1.1} />
            <Tree position={[-7.8, 0, 6.0]} scale={1.2} />
          </group>
        </Center>
      </Canvas>

      {/* Floating HUD Controls */}
      <div className="absolute top-3 right-3 flex items-center gap-2 z-10">
        <button
          onClick={resetCamera}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 text-xs font-medium text-slate-300 border border-white/10 backdrop-blur-md shadow-lg transition-all"
          title="Reset Camera View"
        >
          <RotateCcw className="w-3.5 h-3.5 text-emerald-400" />
          <span>Reset Camera</span>
        </button>
      </div>

      {/* Floating Active Zone Card */}
      {activeZone && (
        <div className="absolute bottom-3 left-3 max-w-sm rounded-lg bg-slate-900/90 border border-white/10 p-3 backdrop-blur-md shadow-2xl z-10">
          <div className="flex items-center justify-between gap-2 border-b border-white/10 pb-2 mb-2">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">{activeZone.name}</span>
            </div>
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800">
              {activeZone.cropType}
            </span>
          </div>

          <div className="grid grid-cols-4 gap-2 text-center text-xs">
            <div className="bg-slate-800/60 p-1.5 rounded">
              <span className="text-[10px] text-slate-400 block">Moisture</span>
              <span className="font-bold text-emerald-400">{activeZone.soilMoisture}%</span>
            </div>
            <div className="bg-slate-800/60 p-1.5 rounded">
              <span className="text-[10px] text-slate-400 block">Temp</span>
              <span className="font-bold text-amber-400">{activeZone.temperature}°C</span>
            </div>
            <div className="bg-slate-800/60 p-1.5 rounded">
              <span className="text-[10px] text-slate-400 block">Humidity</span>
              <span className="font-bold text-sky-400">{activeZone.humidity}%</span>
            </div>
            <div className="bg-slate-800/60 p-1.5 rounded">
              <span className="text-[10px] text-slate-400 block">Rain</span>
              <span className="font-bold text-blue-400">{activeZone.rainfall}mm</span>
            </div>
          </div>

          <div className="mt-2 pt-1.5 border-t border-white/5 flex items-center justify-between text-[11px]">
            <span className="text-slate-400 flex items-center gap-1">
              <Droplets className="w-3 h-3 text-sky-400" />
              Irrigation Risk:
            </span>
            <span className={`font-semibold ${activeZone.irrigationProbability > 0.5 ? 'text-rose-400' : 'text-emerald-400'}`}>
              {(activeZone.irrigationProbability * 100).toFixed(0)}% Probability
            </span>
          </div>
        </div>
      )}

      {/* Live Farmer Status Badge */}
      <div className="absolute top-3 left-3 flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-white/10 text-xs backdrop-blur-md">
        <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
        <span className="text-slate-300 font-medium">Farmer Avatar:</span>
        <span className="text-amber-300 font-semibold">{isIrrigating ? 'Inspecting Valve' : 'Patrolling Rows'}</span>
      </div>

      {/* Irrigation Active Banner Overlay */}
      {isIrrigating && (
        <div className="absolute top-12 left-1/2 -translate-x-1/2 flex items-center gap-2 px-4 py-1.5 rounded-full bg-rose-950/90 border border-rose-500 text-rose-200 text-xs font-bold animate-pulse shadow-xl">
          <Droplets className="w-4 h-4 text-rose-400 animate-bounce" />
          <span>ACTUATOR DIRECTIVE: VALVE_OPEN (IN-SITU IRRIGATION ACTIVE)</span>
        </div>
      )}
    </div>
  );
};
