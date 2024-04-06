<script>
	import retro_style from './map-styles.js';
	export let heatmapData;
	export let renderHeatmap;
	export let startLoc;
	// const { HeatmapLayer, WeightedLocation } = google.maps.importLibrary('visualization');

	let container;
	let map;
	let zoom = 12;
	let center = { lat: 52.51888443, lng: 13.39384 };

	import { onMount } from 'svelte';

	onMount(async () => {
		map = new google.maps.Map(container, {
			zoom,
			center,
			styles: retro_style,
			minZoom: 12,
			maxDefaultZoom: 12, 
		});
	});

	function plotHeatmap() {
		console.log("Start mapping heatmap");
		heatmapData = heatmapData.map((data) => {
			return {location: new google.maps.LatLng(data[0], data[1]), weight: data[2]}
		});
		console.log("Done mapping heatmap");

		var heatmap = new google.maps.visualization.HeatmapLayer({
			data: heatmapData,
			dissipating: true,
			opacity: 0.5,
			maxIntensity: 14000,
		});
		console.log("heatmap layer created");
		heatmap.setMap(map);
		console.log(startLoc);
		let cityCircle = new google.maps.Circle({
			strokeColor: "rgb(0,0,0)",
			strokeOpacity: 0.8,
			strokeWeight: 0,
			fillColor: "rgb(0,0,0)",
			fillOpacity: 1,
			map,
			center: { lat: startLoc.lat, lng: startLoc.lng },
			radius: 100
		});

		console.log("heatmap layer set");
	}
	function plotPoints() {
		let vals = heatmapData.reduce(
			(acc, val) => {
				return [Math.min(acc[0], val[2]), Math.max(acc[1], val[2])];
			},
			[Infinity, -Infinity]
		);
		console.log(vals);

		for (const data in heatmapData) {
			let f = (heatmapData[data][2] - vals[0]) / (vals[1] - vals[0]);

			if (f < 0.5) {
				f = (0.8 * f) / 0.5;
			} else {
				f = 0.8 + (0.2 * (f - 0.5)) / 0.5;
			}

			let c = Math.floor(255 * f);
			let color = `rgb(${c}, ${255 - c}, 0)`;

			// Add the circle for this city to the map.
			let cityCircle = new google.maps.Circle({
				strokeColor: color,
				strokeOpacity: 0.8,
				strokeWeight: 0,
				fillColor: color,
				fillOpacity: 0.5,
				map,
				center: { lat: heatmapData[data][0], lng: heatmapData[data][1] },
				radius: 200
			});
		}
		// heatmap.setMap(map);
	}
</script>

<svelte:head>
	<script
		defer
		async
		src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDc1XXKm-fFJTte3f1B1-qwoTKHYgT3eHo&libraries=visualization&callback=onMount"
	>
	</script>
</svelte:head>

<div id="map" class="full-screen m-auto h-full" bind:this={container}></div>

{#if renderHeatmap}
	<p class="hidden">
		{plotHeatmap()}
	</p>
{:else}{/if}

<style>
	.full-screen {
		width: 60vw;
		height: 80vh;
	}
</style>
