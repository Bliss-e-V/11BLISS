<script>
   let container;
   let map;
   let zoom = 13.2;
   let center = {lat: 52.51888443, lng: 13.39384};
   
   import { onMount } from 'svelte';
   
   onMount(async () => {
       map = new google.maps.Map(container, {
           zoom,
           center,
       });
   });
</script>

<style>
.full-screen {
   width: 60vw;
   height: 80vh;
}
</style>

<div class="full-screen" bind:this={container}></div>