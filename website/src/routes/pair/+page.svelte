
<script>
	import { goto } from "$app/navigation";
	import { promise } from "$lib";

    function pair() {
        // Setup options
        let options = {
            filters: [{namePrefix: "DT Car"},],
            optionalServices: ["0000ffe0-0000-1000-8000-00805f9b34fb"]
        };
        
        // Bluetooth connection
        navigator.bluetooth
        .requestDevice(options)
        .then((device) => {
            console.log(`Connected to: ${device.name}`);
            device.gatt.connect();
            promise.set(device);
            goto("/play");
        })
        .catch((error) => console.error(`Something went wrong. ${error}`));
    }

</script>

<div class="bg-slate-200 sm:bg-slate-400 h-screen w-screen p-10"></div>

<div class="absolute top-0 bottom-0 left-0 right-0 place-self-center bg-slate-200 sm:rounded-xl p-5">
    <h1 class="text-lg">How to pair your bluetooth car...</h1>
    <div class="pl-2 pb-5">
        <p><span class="text-gray-700">1 -</span> Click the pair button</p>
        <p><span class="text-gray-700">2 -</span> A popup will appear asking to pair to a device</p>
        <p><span class="text-gray-700">3 -</span> Press the first one that starts with <span class="italic">DT Car </span></p>
        <p><span class="text-gray-700">4 -</span> Press pair</p>
        <p><span class="text-gray-700">5 -</span> You will be automatically redirected if the device pairs</p>
    </div>
    <button class="bg-neutral-900 rounded-full text-white p-1 pl-5 pr-5" onclick={pair}>I have read the instructions - Pair</button>
</div>