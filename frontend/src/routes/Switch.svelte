<script>
    // based on suggestions from:
    // Inclusive Components by Heydon Pickering https://inclusive-components.design/toggle-button/
    // On Designing and Building Toggle Switches by Sara Soueidan https://www.sarasoueidan.com/blog/toggle-switch-design/
    // and this example by Scott O'hara https://codepen.io/scottohara/pen/zLZwNv


    export let label;
    export let design = 'inner label'


    let checked = true;


		const uniqueID = Math.floor(Math.random() * 100)

    function handleClick(event){
        const target = event.target

        const state = target.getAttribute('aria-checked')

        checked = state === 'true' ? false : true

    }



</script>

{#if design == 'inner'}
<div class="s s--inner">
    <span id={`switch-${uniqueID}`}>{label}</span>
    <button
        type="button"
        role="switch"
        class="rounded-3xl"
        aria-checked={checked}
        aria-labelledby={`switch-${uniqueID}`}
        on:click={handleClick}>
            <span>max</span>
            <span>avg</span>
    </button>
</div>

{/if}

<style>
			:root {
		--accent-color: #F87171;
		--gray: #ccc;
	}
    /* Inner Design Option */
    .s--inner button {
        padding: 0.5em;
        background-color: #fff;
        border: 1px solid var(--accent-color);
    }
    [role='switch'][aria-checked='true'] :first-child,
    [role='switch'][aria-checked='false'] :last-child {
        display: none;
        color: #fff;
    }

    .s--inner button span {
        user-select: none;
        pointer-events:none;
        padding: 0.25em;
    }

    .s--inner button:focus {
        outline: var(--accent-color) solid 1px;
    }

    /* gravy */

    /* Inner Design Option */
    [role='switch'][aria-checked='true'] :first-child,
    [role='switch'][aria-checked='false'] :last-child {
        border-radius: 0.25em;
        background: var(--accent-color);
        display: inline-block;
    }

    .s--inner button:focus {
        box-shadow: 0 0px 8px var(--accent-color);
        border-radius: 0.1em;
    }



</style>