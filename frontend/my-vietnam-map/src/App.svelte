<script>
  import Map from "./components/Map.svelte";
  import Info from "./components/Info.svelte";
  import { selectedProvince } from "./stores.js";
</script>

<main>
  <div class="map-container">
    <Map />
  </div>

  <div class="info-container">
    <Info />
  </div>
</main>

<style>
  main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 90vh;
  }

  @media(min-width: 992px) {
    main {
      flex-direction: row;
      align-items: flex-start;
    }

    .map-container {
      flex: 3;
      position: sticky;
      top: 20px;
    }

    .info-container {
      flex: 2;
    }
  }

  .map-container, .info-container {
    width: 100%;
  }

</style>
