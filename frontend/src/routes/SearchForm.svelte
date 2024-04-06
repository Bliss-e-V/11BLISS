<script>
	// Import any necessary libraries or components
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';

	// Variables related to form fields
	let inputAdr = '';
	let inputDate = '';
	let inputTime = '';

	const dispatch = createEventDispatcher();

	// The getGeocoding function remains unchanged
	function getGeocoding(address) {
		var opts = {
			mode: 'cors'
		};
		return fetch('http://localhost:5000/geocoding?search=' + address, opts)
			.then((response) => response.json())
			.then((data) => {
				return data;
			});
	}

	// Modified handleSubmit to use event dispatch
	function handleSubmit(event) {
		event.preventDefault(); // Prevent the default form submission behavior
		var encodedAddress = encodeURIComponent(inputAdr);

		getGeocoding(encodedAddress).then((geocode) => {
			// Dispatch an event with the geocode result
			dispatch('submit', { geocode: geocode['results'][0]['geometry']['location'] });
		});
	}
</script>

<form method="POST" on:submit={handleSubmit}>
	<label>
		Address
		<input name="address" type="text" bind:value={inputAdr} />
	</label>
	<label>
		Date
		<input name="date" type="date" bind:value={inputDate} />
	</label>
	<label>
		Time
		<input name="time" type="time" bind:value={inputTime} />
	</label>
	<button
		type="submit"
		class="leading-[normal] drop-shadow-lg text-white text-xl text-center flex justify-center bg-red-400 self-stretch p-3.5 rounded-3xl"
		>Search</button
	>
</form>
