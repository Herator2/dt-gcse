// place files you want to import through the `$lib` alias in this folder.

import { goto } from "$app/navigation";
import { writable } from "svelte/store";

export var promise = writable(null);


function hasDevice() {
    if (promise == null) {
        return false;
    } return false; 
}

function isCompatible() {
    return true;
}

export function tryRedirect() {
    if (!isCompatible()) {
        goto("/incompatible");
    } else if (!hasDevice()) {
        goto("/pair");
    }
}



