<svelte:head>
	<script defer async
	src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDc1XXKm-fFJTte3f1B1-qwoTKHYgT3eHo&callback=initMap">
	</script>
</svelte:head>

<script>
    import './+layout.svelte';
    import Map from './Map.svelte';
    let inputAdr = '';
    let inputDate = '';
    let inputTime = '';

    // Function to handle form submission
    function handleSubmit(event) {
      event.preventDefault(); // Prevent the default form submission behavior
      var address = document.getElementsByName('address')[0].value
      var encodedAddress = encodeURIComponent(address)
      console.log(encodedAddress)

      alert('Submitted adress: ' + inputAdr); // For demonstration purposes, alert the input value
      // .then(response => response.json())
      // fetch('http://localhost:5000/geocoding?address=' + encodedAddress)
      // .then(data => {
      //     console.log(data)
      // })

    }

</script>

<nav>
    <div id="logo-container" class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-5 pl-11 pr-14 pt-4 inline-flex w-full`}>
        <img src="logo-bliss-pulse-cropped.svg" alt="blisspuls-logo" width="20%">
    </div>
</nav>
<div  id="central-container" class={`tracking-[0px] font-futura items-start bg-red-100 gap-x-14 flex-row pb-10 pl-11 pr-14 pt-4 inline-flex w-full`}>
    <div id="left-container">
        <div id="search-form">
            <form method="POST" on:submit={handleSubmit}>
                <div class="max-w-md">
                    <div class="mb-4 focus:border-red-400">
                        <input name="address" placeholder="Enter your location here..." class="leading-[normal] drop-shadow-lg text-gray-900 text-xl text-left flex gap-x-16 justify-end items-center bg-white self-stretch py-4 px-2 rounded-3xl w-full" type="text" bind:value={inputAdr}> <!-- Added w-full -->
                    </div>
                    <div id="date_time" class="flex gap-x-4 mb-4">
                        <div class="w-1/2">
                            <input name="date" class="drop-shadow py-[3px] items-center bg-white self-stretch pl-3 pr-2.5 justify-center flex rounded-3xl w-full" type="date" bind:value={inputDate}> <!-- Added w-full -->
                        </div>
                        <div class="w-1/2">
                            <input name="time" class="drop-shadow py-[3px] items-center bg-white self-stretch pl-3 pr-2.5 justify-center flex rounded-3xl w-full" type="time" bind:value={inputTime}> <!-- Added w-full -->
                        </div>
                    </div>
                    <div id="submit_btn">
                        <button type="submit" class="mb-4 leading-[normal] drop-shadow-lg text-white text-xl text-center flex justify-center bg-red-400 self-stretch p-3.5 rounded-3xl w-full">Search</button> <!-- Added w-full -->
                    </div>
                </div>
            </form>

            <div id="text-container" class={`leading-[normal] text-[15px] text-justify`}>
                <p><b>Welcome to BlissPulse &ndash; &quot;Where's the Heat?&quot;</b></p><br>

                <p><i>Discover Berlin's Hidden Gems, Fast.</i></p><br>

                <p>BlissPulse turns Berlin's streets into a dynamic heatmap, showing you nearby spots you can reach in a heartbeat. Explore the city like a local, uncovering hotspots loved by Berliners and visitors alike.</p><br>

                <p><b>Your Neighborhood, Redefined</b></p>

                <p>Find hidden gems just around the corner, guided by our dual heatmap &ndash; showing both proximity and popularity. Explore with insight, discovering quick spots, top-rated venues, and beyond-the-obvious gems.</p><br>

                <p><b>Join the Community</b><br>
                Share your discoveries, rate experiences, and connect with fellow Berlin explorers. With BlissPulse, every street corner tells a story, and your next adventure is just moments away.<br>
                Ready to Feel the Heat?</p><br>

                <p><i>Welcome to BlissPulse &ndash; Where Berlin's pulse meets your curiosity.</i></p>
            </div>
        </div>
    </div>

    <div id="map-container">
        <Map></Map>
    </div>
</div>

<footer class={`bg-red-100 gap-y-14`}>
    <div class="text-center">
        <p><i>Property of Team 3 aka 11Bliss aka Team Memegods</i></p>
    </div>
</footer>





