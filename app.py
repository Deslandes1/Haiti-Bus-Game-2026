import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Race: Haiti Bus vs World",
    page_icon="\U0001F68C",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        iframe {height: 100vh !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Race: Haiti Bus vs World | Gesner Deslandes</title>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', 'Courier New', monospace; }
        #info-panel {
            position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.8);
            backdrop-filter: blur(8px); padding: 12px 20px; border-radius: 16px;
            border-left: 6px solid #D21034; z-index: 100; color: white;
            pointer-events: none; font-weight: bold; text-shadow: 1px 1px 0 black;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 14px;
        }
        .flag-haiti { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
        .flag-rect { width: 40px; height: 24px; background: linear-gradient(to bottom, #00209F 50%, #D21034 50%); border-radius: 4px; border: 1px solid gold; }
        .names { font-size: 12px; line-height: 1.4; }
        .names span { color: #ffd966; }
        #speed-panel {
            position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.7);
            padding: 10px 18px; border-radius: 20px; font-family: monospace; font-size: 22px;
            font-weight: bold; color: #0ff; z-index: 100; backdrop-filter: blur(4px);
            border: 1px solid cyan; pointer-events: none;
        }
        #message-box {
            position: absolute; bottom: 30%; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.85); padding: 12px 24px; border-radius: 40px;
            color: gold; font-weight: bold; font-size: 18px; text-align: center;
            white-space: nowrap; pointer-events: none; z-index: 100;
            font-family: monospace; transition: 0.2s; border: 1px solid #ffaa33;
            backdrop-filter: blur(4px);
        }
        #controls-hint {
            position: absolute; bottom: 20px; left: 20px; background: rgba(0,0,0,0.5);
            padding: 5px 12px; border-radius: 12px; font-size: 12px; color: #ccc;
            font-family: monospace; pointer-events: none;
        }
        .button-group {
            position: absolute; bottom: 30px; right: 20px; display: flex; gap: 12px; z-index: 200;
        }
        button {
            background: #222; color: white;
            border: 1px solid orange; padding: 6px 12px; border-radius: 20px;
            cursor: pointer; font-weight: bold; font-family: monospace;
        }
        button:hover { background: #ff6600; }
        #flag-selector {
            position: absolute; top: 20px; right: 20px; background: rgba(0,0,0,0.7);
            backdrop-filter: blur(8px); padding: 8px 12px; border-radius: 20px;
            color: white; font-family: monospace; z-index: 200;
            display: flex; gap: 8px; align-items: center;
        }
        select { background: #333; color: white; border: 1px solid gold; border-radius: 8px; padding: 4px 8px; }
        @media (max-width: 600px) {
            #info-panel { font-size: 8px; top: 8px; left: 8px; padding: 6px 12px; }
            .names { font-size: 8px; }
            #speed-panel { font-size: 16px; }
            #message-box { font-size: 12px; white-space: nowrap; bottom: 25%;}
            #flag-selector { font-size: 10px; top: 8px; right: 8px; }
        }
    </style>
</head>
<body>
    <div id="info-panel">
        <div class="flag-haiti"><div class="flag-rect"></div><span>🇭🇹 HAITI 🇭🇹</span></div>
        <div class="names">🚌 <span>Gesner Deslandes</span><br>
        👨‍🔧 Gesner Junior Deslandes | Roosevelt Deslandes<br>
        🧑‍🔧 Sebastien Stephane Deslandes | Zendaya Christelle Deslandes</div>
    </div>
    <div id="speed-panel">🚍 SPEED: <span id="speed-value">0</span> km/h</div>
    <div id="message-box">🏁 Choose opponent and press START</div>
    <div id="controls-hint">🎮 [UP] accelerate | [DOWN] brake/reverse | [LEFT/RIGHT] steer | ⚠️ Avoid obstacles!</div>
    <div class="button-group">
        <button id="startBtn">🚦 START RACE</button>
        <button id="resetBtn">🔄 RESET</button>
    </div>
    <div id="flag-selector">
        🏁 Opponent Flag:
        <select id="opponentFlag">
            <option value="dominican">🇩🇴 Dominican Republic</option>
            <option value="usa">🇺🇸 United States</option>
            <option value="france">🇫🇷 France</option>
            <option value="brazil">🇧🇷 Brazil</option>
        </select>
    </div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

        // --- setup scene, camera, renderers ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a1030);
        scene.fog = new THREE.FogExp2(0x0a1030, 0.008);
        
        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 8);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);
        
        const labelRenderer = new CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.left = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none';
        document.body.appendChild(labelRenderer.domElement);
        
        // --- Lighting ---
        const ambientLight = new THREE.AmbientLight(0x404060);
        scene.add(ambientLight);
        const sunLight = new THREE.DirectionalLight(0xfff5d1, 1.2);
        sunLight.position.set(20, 30, 10);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 1024;
        sunLight.shadow.mapSize.height = 1024;
        scene.add(sunLight);
        const fillLight = new THREE.PointLight(0x5577aa, 0.4);
        fillLight.position.set(0, 5, 0);
        scene.add(fillLight);
        
        // --- Race constants ---
        const ROAD_WIDTH = 6.0;
        const LANE_LIMIT = 2.7;
        const FINISH_LINE_Z = 400;
        const START_LINE_Z = 0;
        
        // --- Road (single long plane covering start to finish) ---
        const roadLength = FINISH_LINE_Z + 60;
        const roadMat = new THREE.MeshStandardMaterial({ color: 0x2c2e3a, roughness: 0.7 });
        const roadPlane = new THREE.Mesh(new THREE.PlaneGeometry(ROAD_WIDTH, roadLength), roadMat);
        roadPlane.rotation.x = -Math.PI / 2;
        roadPlane.position.y = -0.05;
        roadPlane.position.z = roadLength/2;
        roadPlane.receiveShadow = true;
        scene.add(roadPlane);
        
        // Lane markings
        const lineMat = new THREE.MeshStandardMaterial({ color: 0xffdd99 });
        for (let z = 5; z <= FINISH_LINE_Z + 20; z += 4) {
            const line = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.05, 2), lineMat);
            line.position.set(0, 0.02, z);
            line.castShadow = false;
            scene.add(line);
        }
        // Edge lines
        const edgeMat = new THREE.MeshStandardMaterial({ color: 0xccaa55 });
        for (let side = -1; side <= 1; side+=2) {
            for (let z = 0; z <= FINISH_LINE_Z + 20; z+=3) {
                const edge = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.08, 1.5), edgeMat);
                edge.position.set(side * (ROAD_WIDTH/2 - 0.25), 0.03, z);
                scene.add(edge);
            }
        }
        
        // Start line (green)
        const startMat = new THREE.MeshStandardMaterial({ color: 0x44aa44 });
        for (let i = -3; i <= 3; i+=1) {
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 1), startMat);
            stripe.position.set(i * 0.6, 0.08, START_LINE_Z);
            scene.add(stripe);
        }
        // Finish line
        const finishMatRed = new THREE.MeshStandardMaterial({ color: 0xdd2222 });
        const finishMatWhite = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
        for (let i = -3; i <= 3; i+=1) {
            const mat = (Math.floor(i) % 2 === 0) ? finishMatRed : finishMatWhite;
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 1), mat);
            stripe.position.set(i * 0.6, 0.08, FINISH_LINE_Z);
            scene.add(stripe);
        }
        const finishDiv = document.createElement('div');
        finishDiv.textContent = '🏁 FINISH 🏁';
        finishDiv.style.color = 'gold';
        finishDiv.style.fontSize = '20px';
        finishDiv.style.fontWeight = 'bold';
        finishDiv.style.backgroundColor = 'rgba(0,0,0,0.6)';
        finishDiv.style.padding = '4px 12px';
        finishDiv.style.borderRadius = '20px';
        finishDiv.style.border = '2px solid red';
        const finishSign = new CSS2DObject(finishDiv);
        finishSign.position.set(0, 1.5, FINISH_LINE_Z);
        scene.add(finishSign);
        
        // --- Obstacles ---
        class Obstacle {
            constructor(z, type) {
                this.type = type;
                let mesh;
                if (type === 'rock') {
                    mesh = new THREE.Mesh(new THREE.DodecahedronGeometry(0.45), new THREE.MeshStandardMaterial({ color: 0x886e4e, roughness: 0.9 }));
                } else {
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 0.6, 5), new THREE.MeshStandardMaterial({ color: 0xbc8f6b }));
                }
                const x = (Math.random() - 0.5) * (ROAD_WIDTH - 1.2);
                mesh.position.set(x, 0.1, z);
                mesh.castShadow = true;
                scene.add(mesh);
                this.mesh = mesh;
                this.z = z;
                this.x = x;
                this.active = true;
            }
            destroy() { scene.remove(this.mesh); }
        }
        
        let obstacles = [];
        for (let z = 50; z <= FINISH_LINE_Z - 30; z += 25) {
            if (Math.abs(z - FINISH_LINE_Z) < 15) continue;
            obstacles.push(new Obstacle(z, Math.random() > 0.6 ? 'rock' : 'log'));
        }
        
        // --- Environment (trees, rocks, cliffs) ---
        const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x8B5A2B });
        const treeTopMat = new THREE.MeshStandardMaterial({ color: 0x5c9e3e });
        const rockMat = new THREE.MeshStandardMaterial({ color: 0x6a705c });
        for (let z = -20; z <= FINISH_LINE_Z + 50; z += 12) {
            for (let side = -1; side <= 1; side+=2) {
                if (Math.random() > 0.6) {
                    const x = side * (ROAD_WIDTH/2 + 1.5 + Math.random() * 3);
                    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.2, 5), treeTrunkMat);
                    trunk.position.set(x, 0.2, z);
                    trunk.castShadow = true;
                    const top = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.0, 6), treeTopMat);
                    top.position.set(x, 0.9, z);
                    top.castShadow = true;
                    scene.add(trunk, top);
                } else if (Math.random() > 0.8) {
                    const x = side * (ROAD_WIDTH/2 + 1.2 + Math.random() * 4);
                    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.5), rockMat);
                    rock.position.set(x, -0.2, z);
                    rock.castShadow = true;
                    scene.add(rock);
                }
            }
        }
        const cliffMat = new THREE.MeshStandardMaterial({ color: 0xaa5533 });
        for (let z = 0; z <= FINISH_LINE_Z + 50; z += 40) {
            if (Math.random() > 0.7) {
                for (let i = -2; i <= 2; i++) {
                    const rock = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8 + Math.random(), 2), cliffMat);
                    rock.position.set(3.8 + i*0.4, -0.2, z + i*1.5);
                    rock.castShadow = true;
                    scene.add(rock);
                }
            }
        }
        
        // --- Bus model (blue & red) - HAITI stays unchanged ---
        const busGroup = new THREE.Group();
        const bodyGeo = new THREE.BoxGeometry(1.4, 0.9, 2.8);
        const blueMatBus = new THREE.MeshStandardMaterial({ color: 0x2a6fdb, roughness: 0.3 });
        const body = new THREE.Mesh(bodyGeo, blueMatBus);
        body.castShadow = true;
        body.position.y = 0.45;
        busGroup.add(body);
        
        const redStripeMatBus = new THREE.MeshStandardMaterial({ color: 0xcc3333 });
        const stripeLeft = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), redStripeMatBus);
        stripeLeft.position.set(-0.75, 0.55, 0);
        busGroup.add(stripeLeft);
        const stripeRight = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), redStripeMatBus);
        stripeRight.position.set(0.75, 0.55, 0);
        busGroup.add(stripeRight);
        const roofStripe = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.1, 2.2), redStripeMatBus);
        roofStripe.position.set(0, 0.9, 0);
        busGroup.add(roofStripe);
        
        const glassMatBus = new THREE.MeshStandardMaterial({ color: 0x88ccff });
        for (let i = -0.8; i <= 0.8; i+=0.8) {
            const win = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.35, 0.08), glassMatBus);
            win.position.set(i, 0.7, 0.9);
            busGroup.add(win);
            const winBack = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.35, 0.08), glassMatBus);
            winBack.position.set(i, 0.7, -0.9);
            busGroup.add(winBack);
        }
        const wheelMatBus = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.7 });
        const wheelGeo = new THREE.CylinderGeometry(0.28, 0.28, 0.4, 16);
        [[-0.8,0.15,1.0],[0.8,0.15,1.0],[-0.8,0.15,-1.1],[0.8,0.15,-1.1]].forEach(pos => {
            const wheel = new THREE.Mesh(wheelGeo, wheelMatBus);
            wheel.rotation.z = Math.PI/2;
            wheel.position.set(pos[0], pos[1], pos[2]);
            wheel.castShadow = true;
            busGroup.add(wheel);
        });
        const lightMatBus = new THREE.MeshStandardMaterial({ color: 0xffaa66, emissive: 0xff4411 });
        const leftLight = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), lightMatBus);
        leftLight.position.set(-0.55, 0.35, 1.45);
        const rightLight = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), lightMatBus);
        rightLight.position.set(0.55, 0.35, 1.45);
        busGroup.add(leftLight, rightLight);
        scene.add(busGroup);
        
        // --- Opponent Car with dynamic flag colors (never Haiti colors) ---
        const carGroup = new THREE.Group();
        const carBodyMesh = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.5, 1.8), new THREE.MeshStandardMaterial({ color: 0xdd4422, roughness: 0.4 }));
        carBodyMesh.position.y = 0.25;
        carGroup.add(carBodyMesh);
        const carRoofMesh = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.3, 1.2), new THREE.MeshStandardMaterial({ color: 0xaa3311 }));
        carRoofMesh.position.y = 0.55;
        carGroup.add(carRoofMesh);
        const wheelMatCar = new THREE.MeshStandardMaterial({ color: 0x222222 });
        [[-0.5,0.1,0.7],[0.5,0.1,0.7],[-0.5,0.1,-0.7],[0.5,0.1,-0.7]].forEach(pos => {
            const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.3, 12), wheelMatCar);
            wheel.rotation.z = Math.PI/2;
            wheel.position.set(pos[0], pos[1], pos[2]);
            wheel.castShadow = true;
            carGroup.add(wheel);
        });
        let extraStripe = null;
        scene.add(carGroup);
        
        // CSS2D flag emoji above car
        let flagDiv = document.createElement('div');
        flagDiv.style.fontSize = '32px';
        flagDiv.style.filter = 'drop-shadow(0 0 2px black)';
        const carFlag = new CSS2DObject(flagDiv);
        carFlag.position.set(0, 0.7, 0);
        carGroup.add(carFlag);
        
        // ---- Opponent Car Dynamic Color Mapping - distinct from Haiti bus ----
        function updateCarColorsByFlag(flagValue) {
            if (extraStripe) {
                carGroup.remove(extraStripe);
                extraStripe = null;
            }
            let bodyColor, roofColor, stripeColor;
            switch(flagValue) {
                case 'dominican': // Dominican Republic: white body, red roof, blue stripe
                    bodyColor = 0xffffff;
                    roofColor = 0xce1126;
                    stripeColor = 0x002b7f;
                    break;
                case 'usa': // USA: red body, white roof, blue stripe
                    bodyColor = 0xb22234;
                    roofColor = 0xffffff;
                    stripeColor = 0x3c3b6e;
                    break;
                case 'france': // France: blue body, white roof, red stripe
                    bodyColor = 0x0055a4;
                    roofColor = 0xffffff;
                    stripeColor = 0xef4135;
                    break;
                case 'brazil': // Brazil: green body, yellow roof, blue stripe
                    bodyColor = 0x009c3b;
                    roofColor = 0xffdf00;
                    stripeColor = 0x002776;
                    break;
                default:
                    bodyColor = 0xdd4422;
                    roofColor = 0xaa3311;
                    stripeColor = null;
            }
            carBodyMesh.material = new THREE.MeshStandardMaterial({ color: bodyColor, roughness: 0.4 });
            carRoofMesh.material = new THREE.MeshStandardMaterial({ color: roofColor, roughness: 0.4 });
            if (stripeColor) {
                const stripeGeo = new THREE.BoxGeometry(0.12, 0.12, 1.6);
                const stripeMat = new THREE.MeshStandardMaterial({ color: stripeColor });
                extraStripe = new THREE.Mesh(stripeGeo, stripeMat);
                extraStripe.position.set(0, 0.38, 0);
                extraStripe.castShadow = true;
                carGroup.add(extraStripe);
            }
        }
        
        function updateOpponentFlagAndColors() {
            const select = document.getElementById('opponentFlag');
            const val = select.value;
            let flagEmoji = '';
            switch(val) {
                case 'dominican': flagEmoji = '🇩🇴'; break;
                case 'usa': flagEmoji = '🇺🇸'; break;
                case 'france': flagEmoji = '🇫🇷'; break;
                case 'brazil': flagEmoji = '🇧🇷'; break;
                default: flagEmoji = '🏁';
            }
            flagDiv.textContent = flagEmoji;
            updateCarColorsByFlag(val);
        }
        updateOpponentFlagAndColors();
        document.getElementById('opponentFlag').addEventListener('change', updateOpponentFlagAndColors);
        
        // --- Race state with pre-start mode ---
        let busZ = 0;
        let carZ = 0;
        let busSpeed = 8;
        let carSpeed = 8;
        let busLateral = -1.0;
        let carLateral = 1.2;
        let crashed = false;
        let raceActive = false;      // becomes true after start button and countdown finishes
        let raceRunning = false;     // indicates if we are actually moving (countdown done)
        let winner = null;
        let countdown = 0;
        let countdownInterval = null;
        
        const MAX_SPEED = 32;
        const MAX_REVERSE = -6;
        const ACCEL = 1.2;
        const BRAKE = 1.6;
        
        let aiTargetSpeed = 12;
        let carSteering = 0;
        
        // DOM elements
        const startBtn = document.getElementById('startBtn');
        const resetBtn = document.getElementById('resetBtn');
        const opponentSelect = document.getElementById('opponentFlag');
        
        function stopCountdown() {
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
        }
        
        function startCountdown() {
            if (countdownInterval) stopCountdown();
            countdown = 3;
            raceRunning = false;
            raceActive = true;
            document.getElementById('message-box').innerHTML = `🏁 Race starts in ${countdown}...`;
            countdownInterval = setInterval(() => {
                if (countdown > 1) {
                    countdown--;
                    document.getElementById('message-box').innerHTML = `🏁 Race starts in ${countdown}...`;
                } else if (countdown === 1) {
                    countdown--;
                    document.getElementById('message-box').innerHTML = `🏁 GO! 🏁`;
                    raceRunning = true;
                    setTimeout(() => {
                        if (raceActive && !winner) {
                            document.getElementById('message-box').innerHTML = `🏁 Race in progress! Use arrows to drive.`;
                        }
                    }, 1500);
                } else {
                    clearInterval(countdownInterval);
                    countdownInterval = null;
                }
            }, 1000);
        }
        
        // Reset everything to pre-start state
        function fullReset() {
            stopCountdown();
            raceActive = false;
            raceRunning = false;
            winner = null;
            crashed = false;
            finishSoundPlayed = false;
            busZ = 0;
            carZ = 0;
            busSpeed = 8;
            carSpeed = 8;
            busLateral = -1.0;
            carLateral = 1.2;
            aiTargetSpeed = 12;
            carSteering = 0;
            busGroup.position.set(busLateral, 0.2, 0);
            carGroup.position.set(carLateral, 0.2, 0);
            // remove balloons
            balloons.forEach(b => scene.remove(b.mesh));
            balloons = [];
            // enable flag selector
            opponentSelect.disabled = false;
            // reset message
            document.getElementById('message-box').innerHTML = "🏁 Choose opponent and press START";
            // ensure start button visible and reset button works
            startBtn.disabled = false;
            startBtn.style.opacity = '1';
            // reset speed display
            document.getElementById('speed-value').innerText = "0";
        }
        
        // Start the race (called when start button clicked)
        function startRace() {
            if (raceActive) return; // already racing or counting down
            fullReset();           // ensure clean state
            // disable opponent selection during race
            opponentSelect.disabled = true;
            // start countdown and enable movement after countdown
            startCountdown();
        }
        
        // Enhanced AI obstacle avoidance
        function updateAI(dt) {
            if (!raceRunning) return;
            const lookahead = 35;
            let nearestObstacle = null;
            let minDist = Infinity;
            for (let obs of obstacles) {
                if (!obs.active) continue;
                const dist = obs.z - carZ;
                if (dist > 0 && dist < lookahead && Math.abs(obs.x - carLateral) < 1.2) {
                    if (dist < minDist) {
                        minDist = dist;
                        nearestObstacle = obs;
                    }
                }
            }
            if (nearestObstacle) {
                if (nearestObstacle.x > carLateral) carSteering = -1.2;
                else carSteering = 1.2;
            } else {
                if (carLateral < 1.0) carSteering = 0.8;
                else if (carLateral > 1.4) carSteering = -0.8;
                else carSteering = 0;
            }
            carLateral += carSteering * dt * 2.5;
            carLateral = Math.max(-LANE_LIMIT + 0.5, Math.min(LANE_LIMIT - 0.5, carLateral));
            let obstacleAhead = (nearestObstacle !== null);
            if (obstacleAhead) aiTargetSpeed = Math.max(5, aiTargetSpeed - 5 * dt);
            else aiTargetSpeed = Math.min(MAX_SPEED - 2, aiTargetSpeed + 3 * dt);
            if (carSpeed < aiTargetSpeed) carSpeed += ACCEL * dt;
            else if (carSpeed > aiTargetSpeed) carSpeed -= BRAKE * dt;
            carSpeed = Math.max(MAX_REVERSE, Math.min(MAX_SPEED, carSpeed));
            carZ += carSpeed * dt;
            carGroup.position.x = carLateral;
            carGroup.position.z = carZ;
            carGroup.position.y = 0.2;
        }
        
        const keys = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false };
        window.addEventListener('keydown', (e) => {
            if (e.key.startsWith('Arrow')) e.preventDefault();
            if (!raceRunning && !(e.key === 'ArrowUp' && winner)) return; // only accept input when race is running
            keys[e.key] = true;
        });
        window.addEventListener('keyup', (e) => { if (e.key.startsWith('Arrow')) keys[e.key] = false; });
        
        function updateBus(dt) {
            if (!raceRunning) return;
            if (keys.ArrowUp) {
                busSpeed += ACCEL * dt;
                if (busSpeed > MAX_SPEED) busSpeed = MAX_SPEED;
            }
            if (keys.ArrowDown) {
                if (busSpeed > 0) busSpeed -= BRAKE * dt;
                else busSpeed -= ACCEL * 0.9 * dt;
                if (busSpeed < MAX_REVERSE) busSpeed = MAX_REVERSE;
            }
            if (!keys.ArrowUp && !keys.ArrowDown && busSpeed !== 0) {
                busSpeed *= (1 - dt * 1.2);
                if (Math.abs(busSpeed) < 0.2) busSpeed = 0;
            }
            let turn = 0;
            if (keys.ArrowLeft) turn = -5.5;
            if (keys.ArrowRight) turn = 5.5;
            busLateral += turn * dt * (Math.abs(busSpeed) * 0.1 + 0.7);
            busLateral = Math.max(-LANE_LIMIT, Math.min(LANE_LIMIT, busLateral));
            busGroup.position.x = busLateral;
            busZ += busSpeed * dt;
            busGroup.position.z = busZ;
            busGroup.position.y = 0.2;
        }
        
        function checkCollisions() {
            if (!raceRunning) return;
            const busX = busLateral;
            const carX = carLateral;
            for (let obs of obstacles) {
                if (!obs.active) continue;
                if (Math.abs(obs.z - busZ) < 1.2 && Math.abs(obs.x - busX) < 0.9) {
                    crashed = true;
                    raceRunning = false;
                    raceActive = false;
                    showMessage(`💥 Bus crashed! Press RESET.`, true);
                    return;
                }
                if (Math.abs(obs.z - carZ) < 1.2 && Math.abs(obs.x - carX) < 0.8) {
                    crashed = true;
                    raceRunning = false;
                    raceActive = false;
                    showMessage(`💥 Opponent crashed! Press RESET.`, true);
                    return;
                }
            }
            if (Math.abs(busLateral) > LANE_LIMIT) {
                crashed = true;
                raceRunning = false;
                raceActive = false;
                showMessage(`💥 Bus drove off road! Press RESET.`, true);
                return;
            }
        }
        
        let finishSoundPlayed = false;
        function playFinishFanfare(winnerName) {
            if (finishSoundPlayed) return;
            finishSoundPlayed = true;
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            let ctx = null;
            try {
                ctx = new AudioCtx();
            } catch(e) { return; }
            const now = ctx.currentTime;
            const masterGain = ctx.createGain();
            masterGain.gain.value = 0.5;
            masterGain.connect(ctx.destination);
            
            const notes = [261.63, 329.63, 392.00, 523.25];
            const durations = [0.25, 0.25, 0.25, 0.6];
            for (let i = 0; i < notes.length; i++) {
                const osc = ctx.createOscillator();
                const gainNote = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = notes[i];
                gainNote.gain.setValueAtTime(0.3, now + i * 0.28);
                gainNote.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.28 + durations[i]);
                osc.connect(gainNote);
                gainNote.connect(masterGain);
                osc.start(now + i * 0.28);
                osc.stop(now + i * 0.28 + durations[i]);
            }
            const noise = ctx.createBufferSource();
            const bufferSize = 4096;
            const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
            noise.buffer = buffer;
            const noiseGain = ctx.createGain();
            noiseGain.gain.setValueAtTime(0.2, now + 0.4);
            noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
            noise.connect(noiseGain);
            noiseGain.connect(masterGain);
            noise.start(now + 0.4);
            noise.stop(now + 1.2);
            
            const drum = ctx.createOscillator();
            drum.type = 'triangle';
            drum.frequency.value = 150;
            const drumGain = ctx.createGain();
            drumGain.gain.setValueAtTime(0.4, now);
            drumGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.2);
            drum.connect(drumGain);
            drumGain.connect(masterGain);
            drum.start(now);
            drum.stop(now + 0.2);
        }
        
        function checkFinish() {
            if (!raceRunning) return;
            if (busZ >= FINISH_LINE_Z && winner === null) {
                winner = 'bus';
                raceRunning = false;
                raceActive = false;
                showMessage(`🏆 HAITI BUS WINS! 🎉🏆`, false);
                playFinishFanfare('bus');
                createBalloons();
                opponentSelect.disabled = false; // allow new selection after race
            } else if (carZ >= FINISH_LINE_Z && winner === null) {
                winner = 'car';
                raceRunning = false;
                raceActive = false;
                showMessage(`🏆 OPPONENT CAR WINS! Better luck next time! 🏆`, false);
                playFinishFanfare('car');
                createBalloons();
                opponentSelect.disabled = false;
            }
        }
        
        function resetRace() {
            fullReset();
            opponentSelect.disabled = false;
            startBtn.disabled = false;
            startBtn.style.opacity = '1';
        }
        
        let balloons = [];
        function createBalloons() {
            for (let i = 0; i < 20; i++) {
                const color = new THREE.Color().setHSL(Math.random(), 0.8, 0.6);
                const balloonMat = new THREE.MeshStandardMaterial({ color: color });
                const balloon = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 16), balloonMat);
                const x = (Math.random() - 0.5) * 6;
                const z = FINISH_LINE_Z + (Math.random() - 0.5) * 5;
                balloon.position.set(x, 0.5, z);
                scene.add(balloon);
                balloons.push({ mesh: balloon, lift: 0, speed: 0.5 + Math.random() * 0.5 });
            }
        }
        
        function updateBalloons(dt) {
            for (let i=0; i<balloons.length; i++) {
                const b = balloons[i];
                b.lift += dt * b.speed;
                b.mesh.position.y = 0.5 + b.lift;
                if (b.mesh.position.y > 8) {
                    scene.remove(b.mesh);
                    balloons.splice(i,1);
                    i--;
                }
            }
        }
        
        const speedSpan = document.getElementById('speed-value');
        const msgBox = document.getElementById('message-box');
        let messageTimeout = null;
        function showMessage(text, isWarning = false, duration = 2500) {
            if (messageTimeout) clearTimeout(messageTimeout);
            msgBox.innerHTML = text;
            msgBox.style.color = isWarning ? '#ff8866' : '#ffdd99';
            messageTimeout = setTimeout(() => {
                if (!raceActive && !winner) msgBox.innerHTML = "Race over. Press RESET.";
                else if (raceActive && raceRunning) msgBox.innerHTML = "🏁 Race in progress! Use arrows to drive.";
                else if (!raceActive) msgBox.innerHTML = "Choose opponent and press START";
            }, duration);
        }
        
        startBtn.addEventListener('click', startRace);
        resetBtn.addEventListener('click', resetRace);
        
        let engineOsc = null, engineGain = null;
        function initEngineSound() {
            if (engineOsc) return;
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            engineOsc = ctx.createOscillator();
            engineGain = ctx.createGain();
            engineOsc.type = 'sawtooth';
            engineOsc.frequency.value = 60;
            engineGain.gain.value = 0;
            engineOsc.connect(engineGain);
            engineGain.connect(ctx.destination);
            engineOsc.start();
            window.engineCtx = ctx;
        }
        function updateEngineSound(speed) {
            if (!engineOsc || !window.engineCtx) return;
            if (window.engineCtx.state === 'suspended') window.engineCtx.resume();
            const absSpd = Math.abs(speed);
            const norm = Math.min(1, absSpd / MAX_SPEED);
            engineOsc.frequency.value = 55 + norm * 140;
            engineGain.gain.value = absSpd > 0.5 ? 0.1 + norm * 0.2 : 0;
        }
        
        function updateCamera() {
            const targetX = busLateral * 0.3;
            const targetY = 3.5 + Math.min(1.2, Math.abs(busSpeed)/20) * 0.5;
            const targetZ = busZ - 6;
            camera.position.lerp(new THREE.Vector3(targetX, targetY, targetZ), 0.1);
            camera.lookAt(busLateral, 1.0, busZ);
        }
        
        let lastTime = performance.now();
        function animate() {
            const now = performance.now();
            let dt = Math.min(0.033, (now - lastTime) / 1000);
            lastTime = now;
            
            if (raceRunning && !crashed) {
                updateBus(dt);
                updateAI(dt);
                checkCollisions();
                checkFinish();
                updateEngineSound(busSpeed);
                speedSpan.innerText = Math.floor(Math.abs(busSpeed) * 3.6);
            }
            updateBalloons(dt);
            updateCamera();
            
            renderer.render(scene, camera);
            labelRenderer.render(scene, camera);
            requestAnimationFrame(animate);
        }
        
        window.addEventListener('keydown', () => {
            if (!engineOsc) initEngineSound();
            if (window.engineCtx && window.engineCtx.state === 'suspended') window.engineCtx.resume();
        });
        
        fullReset(); // initial pre-start state
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>

"""

components.html(GAME_HTML, height=900, scrolling=False)
