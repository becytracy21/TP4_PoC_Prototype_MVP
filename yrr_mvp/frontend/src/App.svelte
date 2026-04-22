<script lang="ts">
  import Bateaux from './Bateaux.svelte';
  import Course from './Course.svelte';
  let page: 'bateaux' | 'course' = 'bateaux';

  function handleNavigate(e: CustomEvent) {
    if (e.detail === 'course') page = 'course';
    else page = 'bateaux'; // fallback simple
  }
</script>

{#if page === 'bateaux'}
  <Bateaux on:navigate={handleNavigate} />
{:else if page === 'course'}
  <Course on:navigate={handleNavigate} />
{/if}