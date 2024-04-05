<script>
    import './+layout.svelte';

    let inputValue = ''; // Initialize a variable to hold the input value

    // Function to handle form submission
    function handleSubmit(event) {
      event.preventDefault(); // Prevent the default form submission behavior
      var address = document.getElementsByName('address')[0].value
      var encodedAddress = encodeURIComponent(address)
      console.log(encodedAddress)
      sleep(1000)

      alert('Submitted value: ' + inputValue); // For demonstration purposes, alert the input value
      // .then(response => response.json())
      // fetch('http://localhost:5000/geocoding?address=' + encodedAddress)
      // .then(data => {
      //     console.log(data)
      // })

    }

</script>

<nav>
    <div class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}>
        <p>Hello world</p>
    </div>
</nav>
<div class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}>
    <div >
        <div>
            <form method="POST"  on:submit={handleSubmit}   >
                <label>
                    Address
                    <input name="address" type="text" bind:value={inputValue}>
                </label>
                <button type="submit">Search</button>
            </form>
            <div>
                <p>Lorem impsum</p>
            </div>
        </div>

        <div>

            <p>{inputValue}</p>
        </div>
    </div>
</div>

<footer class={`tracking-[0px] font-futura items-start bg-red-100 gap-y-14 flex-col pb-20 pl-11 pr-14 pt-4 inline-flex w-full`}>
    <p>hello world</p>
</footer>





