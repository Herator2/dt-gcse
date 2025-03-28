



<h1 class="text-slate-800 text-2xl">GCSE DT CONTROLLER</h1>

<button id="button-on">
    ON
</button>

<button id="button-off">
    OFF
</button>

<h2>Supported Browsers*</h2>
<div>
    <p class="text-slate-900"> - Chrome** <span class="text-slate-500">(RECOMMENDED)</span></p>
    <p class="text-slate-900"> - Edge (>79)</p>
    <p class="text-slate-900"> - Opera (>43)</p>
    <p class="text-slate-900"> - Samsung Internet (>56)</p>
</div>
<p>*Firefox and safari are <span class="text-red-700">not</span> supported.</p>
<p>**This does <span class="text-red-700">not</span> include the google app.</p>



<script>
	import { onMount } from "svelte";

    onMount(() => {
        // Contains all the code for this project
        document.getElementById("button-on")?.addEventListener("click", enableLed)
        document.getElementById("button-off")?.addEventListener("click", disableLed)
    })


    function getDevice() {
        let options = {
            acceptAllDevices: true,
            //filters: [{ services: [0x00805f9b34fb] },],
        };
        
        navigator.bluetooth
        .requestDevice(options)
        .then((device) => {
            console.log(`Name: ${device.name}`);
            // Do something with the device.
        })
        .catch((error) => console.error(`Something went wrong. ${error}`));
    }


    function enableLed() {
        console.log("LED ENABLED")
        getDevice()
    }

    function disableLed() {
        console.log("LED DISABLED")
    }

    
</script>

