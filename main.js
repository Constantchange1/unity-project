import * as THREE from 'three';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0x404040); // soft white light
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
scene.add(directionalLight);

// Torus Parameters
const R = 5; // Major radius
const r = 1; // Minor radius
const radialSegments = 64;
const tubularSegments = 32;

// Torus Geometry and Material
const geometry = new THREE.TorusGeometry(R, r, radialSegments, tubularSegments);
const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 }); // Green color
const torus = new THREE.Mesh(geometry, material);
scene.add(torus);

// Camera Position
camera.position.z = 15;

// Animation Loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate the torus (optional)
    torus.rotation.x += 0.01;
    torus.rotation.y += 0.01;

    renderer.render(scene, camera);
}

animate();