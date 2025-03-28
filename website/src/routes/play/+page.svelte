<script>

    import { promise } from "$lib";

    var value = $promise
    console.log(value)

    function writeData(data) {
        return value.gatt.connect()
        .then(server => server.getPrimaryService("0000ffe0-0000-1000-8000-00805f9b34fb"))
        .then(service => service.getCharacteristic("0000ffe1-0000-1000-8000-00805f9b34fb"))
        .then(characteristic => {
            characteristic.writeValue(Uint8Array.of(data));
            console.log("Sent:", data);
        })
        .catch(err => console.log(err))
    }
</script>

<style>
    .prevent-select {
        -webkit-user-select: none; /* Safari */
        -ms-user-select: none; /* IE 10 and IE 11 */
        user-select: none; /* Standard syntax */
    }
</style>

<div class="absolute top-0 left-0 p-2">
    <p>Status: <span class="text-emerald-700">Connected</span></p>
    <p>Name: <span class="text-neutral-600">{value.name}</span></p>
    <p>Instruction: <span class="text-neutral-600">1</span></p>
    <p>LED control:
        <button class="text-neutral-600 hover:text-neutral-800" onclick={() => writeData("1")}>on</button>
        <button class="text-neutral-600 hover:text-neutral-800" onclick={() => writeData("0")}>off</button>
    </p>
</div>

<div class="absolute top-0 bottom-0 right-0 left-0 place-self-center bg-slate-200 rounded-xl">
    <div class="grid grid-cols-3 grid-rows-3 h-64 w-64 gap-2">
        <p></p>
        <button class="bg-neutral-900 rounded-xl text-neutral-100 active:bg-emerald-500 active:scale-95 transition-all prevent-select" onclick={() => writeData("10")}>Forward</button>
        <p></p>
        <button class="bg-neutral-900 rounded-xl text-neutral-100 active:bg-emerald-500 active:scale-95 transition-all prevent-select" onclick={() => writeData("11")}>Left</button>
        <button class="bg-neutral-900 rounded-xl text-neutral-100 active:bg-emerald-500 active:scale-95 transition-all prevent-select" onclick={() => writeData("14")}>Stop</button>
        <button class="bg-neutral-900 rounded-xl text-neutral-100 active:bg-emerald-500 active:scale-95 transition-all prevent-select" onclick={() => writeData("12")}>Right</button>
        <p></p>
        <button class="bg-neutral-900 rounded-xl text-neutral-100 active:bg-emerald-500 active:scale-95 transition-all prevent-select" onclick={() => writeData("13")}>Reverse</button>
        <p></p>
    </div>
</div>
