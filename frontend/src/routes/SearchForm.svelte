<script>
	// Import any necessary libraries or components
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';
	import Switch from './Switch.svelte';

	let switchValue;

	let inputAdr = '';
	let inputDate = '';
	let inputTime = '';
	let addressCount = 1; // Track the number of address fields added

	function addAddress() {
		if (addressCount < 4) {
			// Maximum 4 addresses allowed
			const addressContainer = document.getElementById('address_container');
			const newAddressInput = document.createElement('div');
			newAddressInput.innerHTML = `
                <div class="flex gap-x-4 mb-4">
                    <input name="address${addressCount + 1}" placeholder="Enter your location here..." class="leading-[normal] drop-shadow-lg text-blue-600 text-left flex gap-x-16 justify-end items-center bg-white self-stretch py-4 px-2 rounded-3xl w-full" type="text">
                    <button type="button" class="remove-address-btn ml-2 leading-[normal] drop-shadow-lg text-red-600 text-left flex justify-center items-center self-stretch py-3 px-4 rounded-3xl">-remove address</button>
                </div>`;
			addressContainer.appendChild(newAddressInput);
			addressCount++;
			newAddressInput
				.querySelector('.remove-address-btn')
				.addEventListener('click', () => removeAddress(newAddressInput));
			if (addressCount >= 4) {
				document.getElementById('add_address_button_wrapper').style.display = 'none';
			}
		}
	}

	function removeAddress(addressInput) {
		if (addressCount > 1) {
			// Minimum 1 address allowed
			addressInput.remove();
			addressCount--;
			if (addressCount < 4) {
				document.getElementById('add_address_button_wrapper').style.display = 'flex';
			}
		}
	}

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
	<div class="max-w-md">
		<div id="switch" class="mb-2">
			<Switch bind:value={switchValue} label="" design="inner" />
		</div>
		<div id="address_container">
			<!-- Existing address input fields will be appended here -->
			<div class="flex gap-x-4 mb-4">
				<input
					name="address"
					placeholder="Enter your location here..."
					class="leading-[normal] drop-shadow-lg text-gray-900 text-xl text-left flex gap-x-16 justify-end items-center bg-white self-stretch py-4 px-2 rounded-3xl w-full"
					type="text"
					bind:value={inputAdr}
				/>
			</div>
		</div>
		<div class="flex justify-between" id="add_address_button_wrapper">
			<button
				type="button"
				on:click={addAddress}
				class="leading-[normal] drop-shadow-lg text-blue-600 text-left flex justify-center items-center self-stretch mb-1"
				>+ add address</button
			>
		</div>
		<div id="date_time" class="flex gap-x-4 mb-4">
			<div
				class="w-1/2 drop-shadow flex gap-x-4 py-[3px] items-center bg-white pl-3 pr-2.5 justify-between rounded-3xl w-full"
			>
				<input name="date" class="" type="date" bind:value={inputDate} />
				<img src="calendar-icon.svg" alt="Calendar" width="10%" />
			</div>
			<div
				class="w-1/2 w-1/2 drop-shadow flex gap-x-4 py-[3px] items-center bg-white pl-3 pr-2.5 justify-between rounded-3xl w-full"
			>
				<input name="time" class="" type="time" bind:value={inputTime} />
				<img src="time-icon.svg" alt="Time" width="10%" />
			</div>
		</div>
		<div id="submit_btn">
			<button
				type="submit"
				class="mb-4 leading-[normal] drop-shadow-lg text-white text-xl text-center flex justify-center bg-red-400 self-stretch p-3.5 rounded-3xl w-full"
				>Search</button
			>
		</div>
	</div>
</form>

<div id="text-container" class={`leading-[normal] text-[15px] text-justify`}>
	<p><b>Welcome to BlissPulse &ndash; &quot;Where's the Heat?&quot;</b></p>
	<br />

	<p><i>Discover Berlin's Hidden Gems, Fast.</i></p>
	<br />

	<p>
		BlissPulse turns Berlin's streets into a dynamic heatmap, showing you nearby spots you can reach
		in a heartbeat. Explore the city like a local, uncovering hotspots loved by Berliners and
		visitors alike.
	</p>
	<br />

	<p><b>Your Neighborhood, Redefined</b></p>

	<p>
		Find hidden gems just around the corner, guided by our dual heatmap &ndash; showing both
		proximity and popularity. Explore with insight, discovering quick spots, top-rated venues, and
		beyond-the-obvious gems.
	</p>
	<br />

	<p>
		<b>Join the Community</b><br />
		Share your discoveries, rate experiences, and connect with fellow Berlin explorers. With BlissPulse,
		every street corner tells a story, and your next adventure is just moments away.<br />
		Ready to Feel the Heat?
	</p>
	<br />

	<p><i>Welcome to BlissPulse &ndash; Where Berlin's pulse meets your curiosity.</i></p>
</div>
