<script>
	import './+layout.svelte';
	import Map from './Map.svelte';
	let inputAdr = '';
	let inputDate = '';
	let inputTime = '';

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

	// Function to handle form submission
	function handleSubmit(event) {
		event.preventDefault(); // Prevent the default form submission behavior
		var encodedAddress = encodeURIComponent(inputAdr);
		console.log(encodedAddress);

		getGeocoding(encodedAddress).then((geocode) => {
			console.log(geocode['results'][0]['geometry']['location']);
		});
	}
</script>

<svelte:head>
	<script
		defer
		async
		src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDc1XXKm-fFJTte3f1B1-qwoTKHYgT3eHo&callback=initMap"
	>
	</script>
</svelte:head>

<nav>
	<div
		id="logo-container"
		class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}
	>
		<img src="logo-bliss-pulse.svg" alt="blisspuls-logo" />
	</div>
</nav>
<div
	id="central-container"
	class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}
>
	<div id="left-container">
		<div id="search-form">
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
			<div id="text-container">
				<p>Lorem impsum</p>
			</div>
		</div>
	</div>
	<div>
		<div id="map-container">
			<Map></Map>
			<p>{inputAdr}</p>
			<p>{inputDate}</p>
			<p>{inputTime}</p>
		</div>
	</div>
</div>

<footer
	class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}
>
	<p>hello world</p>
</footer>
