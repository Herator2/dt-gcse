<script lang="ts">
	import { onMount } from 'svelte';
	import { tryRedirect } from "$lib/index"
	import '../app.css';
	let { children } = $props();

	onMount(tryRedirect)

</script>

<div class="bg-slate-200 w-full h-screen">
	{@render children()}
</div>
<p class="absolute bottom-0 p-2">This website is for my GCSE Eduqas DT NEA.<br>Made by Alexander Van der Ent.</p>
