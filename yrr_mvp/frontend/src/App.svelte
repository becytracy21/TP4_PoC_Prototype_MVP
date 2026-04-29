<script lang="ts">
  import Bateaux from './Bateaux.svelte';
  import Course from './Course.svelte';
  import Inscription from './Inscription.svelte';
  let page: 'bateaux' | 'course' | 'inscription' = 'bateaux';

  function handleNavigate(e: CustomEvent) {
    if (e.detail === 'course') page = 'course';
    else if (e.detail === 'inscription') page = 'inscription';
    else page = 'bateaux'; // fallback simple
  }
</script>

{#if page === 'bateaux'}
  <Bateaux on:navigate={handleNavigate} />
{:else if page === 'course'}
  <Course on:navigate={handleNavigate} />
{:else if page === 'inscription'}
  <Inscription on:navigate={handleNavigate} />
{/if}