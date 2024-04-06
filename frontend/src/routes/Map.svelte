<script>
   let container;
   let map;
   let zoom = 13.2;
   let center = {lat: 52.51888443, lng: 13.39384};
   import retro_style from './map-styles.js'
   import { onMount } from 'svelte';
   
   onMount(async () => {
       map = new google.maps.Map(container, {
           zoom,
           center,
           styles: retro_style
       });
       const transitLayer = new google.maps.TransitLayer();

       transitLayer.setMap(map);

   });
</script>

<style>
.full-screen {
   width: 60vw;
   height: 80vh;
}
</style>

<div class="full-screen m-auto h-full" bind:this={container}></div>