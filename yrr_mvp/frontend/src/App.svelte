<script lang="ts">
  import Bateaux from './Bateaux.svelte';
  import Inscription from './Inscription.svelte';

  let page: 'inscription' | 'bateaux' = 'inscription';
</script>

{#if page === 'inscription'}
  <Inscription onSuccess={() => (page = 'bateaux')} />
{:else}
  <Bateaux />
{/if}