<script>
	import './+layout.svelte';
	import Map from './Map.svelte';
	import SearchForm from './SearchForm.svelte'; // Import the new components
	let heatmapData = [[52, 13, 10]]; // Initialize heatmapData as an empty array
	let renderHeatmap = false;
</script>

<nav class={`border-b-2 border-slate-950`}>
    <div id="logo-container" class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-5 pl-11 pr-14 pt-4 inline-flex w-full`}>
        <img src="logo-bliss-pulse-sonnenbrille.png" alt="blisspuls-logo" width="20%">
    </div>
</nav>
<div
	id="central-container"
	class={`tracking-[0px] font-futura items-start bg-red-100 gap-x-14 flex-row pb-10 pl-11 pr-14 pt-4 inline-flex w-full`}
>
	<div id="left-container">
		<SearchForm
			on:submit={async (event) => {
				// Handle the submission event, event.detail.geocode contains the geocode result

				// Handle the submission event, event.detail.geocode contains the geocode result
				console.log(event.detail.geocode);
				heatmapData = await fetch(
					`http://localhost:5000/gridtimes?starts=[(${event.detail.geocode.lat},${event.detail.geocode.lng})]`
				).then((data) => {
					return data.json(); // Update the heatmapData variable with the fetched data
				});

				renderHeatmap = true; // Set renderHeatmap to true to display the heatmap
			}}
		/>
	</div>

	<div id="right-container">
		<Map {heatmapData} {renderHeatmap} />
	</div>
</div>

<footer class={`bg-red-100 gap-y-14 pt-4 border-t-2 border-slate-950`}>
    <div class="text-center">
        <p>Property of Team 3 aka 11Bliss aka Team Memegods</p>
    </div>
</footer>
