// Drag & Drop
const dropzone = document.getElementById("dropzone")
const fileInput = document.getElementById("image")
const preview = document.getElementById("preview")

dropzone.addEventListener("click", () => fileInput.click())
fileInput.addEventListener("change", function(){
    const file = this.files[0]
    if(file){
        const reader = new FileReader()
        reader.onload = function(e){
            preview.src = e.target.result
            preview.style.display = "block"
        }
        reader.readAsDataURL(file)
    }
})
dropzone.addEventListener("dragover", e=>{
    e.preventDefault()
    dropzone.style.background="rgba(255,255,255,0.2)"
})
dropzone.addEventListener("dragleave", e=>{
    e.preventDefault()
    dropzone.style.background="transparent"
})
dropzone.addEventListener("drop", e=>{
    e.preventDefault()
    fileInput.files = e.dataTransfer.files
    const file = e.dataTransfer.files[0]
    const reader = new FileReader()
    reader.onload = function(e){
        preview.src = e.target.result
        preview.style.display="block"
    }
    reader.readAsDataURL(file)
})

// Loader
const form = document.querySelector("form");
const loader = document.getElementById("loader");
form.addEventListener("submit", () => loader.classList.remove("hidden"));

// Dark / Light toggle
const toggle = document.getElementById("theme-toggle");
toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
});

// 3D Tilt Card
const containerInner = document.querySelector(".container-inner");
containerInner.addEventListener("mousemove", (e) => {
    const rect = containerInner.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = ((y / rect.height) - 0.5) * 15;
    const rotateY = ((x / rect.width) - 0.5) * 15;
    containerInner.style.transform = `rotateX(${-rotateX}deg) rotateY(${rotateY}deg)`;
});
containerInner.addEventListener("mouseleave", () => {
    containerInner.style.transform = "rotateX(0deg) rotateY(0deg)";
});

// Animate price and confidence
window.addEventListener("load", () => {
    const meterFill = document.getElementById("meter-fill");
    if(meterFill){
    let width = meterFill.dataset.width;
    meterFill.style.width = width;
}

    const resultElem = document.querySelector("#result-container h2");
    if(resultElem){
        const priceText = resultElem.textContent.replace(/[^0-9]/g,"");
        let price = parseInt(priceText);
        let count = 0;
        const increment = Math.ceil(price/100);
        resultElem.textContent = "$0";
        const counter = setInterval(()=>{
            count+=increment;
            if(count>=price){count=price;clearInterval(counter);}
            resultElem.textContent = `$${count.toLocaleString()}`;
        },20);
    }
});

// Initialize tsParticles
tsParticles.load("tsparticles", {
    fpsLimit: 60,
    background: { color: "transparent" },
    particles: {
        number: { value: 50 },
        color: { value: "#ffffff" },
        shape: { type: "circle" },
        opacity: { value: 0.5 },
        size: { value: { min: 2, max: 5 } },
        move: { enable: true, speed: 1, random: true, straight: false, outModes: "out" }
    },
    interactivity: { events: { onHover: { enable: true, mode: "repulse" } }, modes: { repulse: { distance: 80, duration: 0.4 } } }
});

// Sparkle effect on drag-drop
dropzone.addEventListener("mousemove", (e) => {
    const sparkle = document.createElement("div");
    sparkle.classList.add("sparkle");
    sparkle.style.left = `${e.offsetX}px`;
    sparkle.style.top = `${e.offsetY}px`;
    dropzone.appendChild(sparkle);
    setTimeout(()=>sparkle.remove(),500);
});
form.addEventListener("submit", (e) => {
    const area = document.querySelector("input[name='area']").value;
    if(area <= 0){
        alert("Area must be greater than 0");
        e.preventDefault();
    }
});