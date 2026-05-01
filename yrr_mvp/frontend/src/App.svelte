<script lang="ts">
  import Bateaux from './Bateaux.svelte';
  import Course from './Course.svelte';
  import Inscription from './Inscription.svelte';
  let page: 'bateaux' | 'course' | 'inscription' = 'bateaux';

 function handleNavigate(e: CustomEvent) {
  const target = e.detail;

  if (target === 'course') {
    page = 'course';
  } 
  else if (target === 'inscription') {
    page = 'inscription';
  } 
  else if (target === 'bateaux') {
    page = 'bateaux';
  } 
  else {
    console.warn('Page inconnue:', target);
  }
}
</script>

{#if page === 'bateaux'}
  <Bateaux on:navigate={handleNavigate} />
{:else if page === 'course'}
  <Course on:navigate={handleNavigate} />
{:else if page === 'inscription'}
  <Inscription on:navigate={handleNavigate} />
{/if}