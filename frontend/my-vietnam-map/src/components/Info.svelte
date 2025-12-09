<script>
  import { selectedProvince } from '../stores.js';
  import { onMount } from 'svelte';
  import { getPlacesByProvince } from "../api/tourism.js";
  import { getHotelsNearPlace } from "../api/hotel.js"; 

  $: province = $selectedProvince;
  $: filteredPlaces = [];

  let selectedCategories = ['all'];
  let allPlaces = [];
  let selectedPlace = null;
  let minRating = 0;
  let isLoading = false;
  let isLoadingHotels = false;
  let hotels = [];
  let showHotels = false;

  const categories = [
    { id: 'all', label: 'Tất cả' },
    { id: 'Thiên nhiên', label: 'Thiên nhiên' },
    { id: 'Tâm linh', label: 'Tâm linh' },
    { id: 'historical', label: 'Lịch sử' },
    { id: 'natural', label: 'Tự nhiên' }
  ];

  async function loadPlacesData() {
    if (!province) return;

    isLoading = true;
    console.log(`[LOAD] Loading places for: ${province}`);
    
    try {
      allPlaces = await getPlacesByProvince(province);
      console.log(`[LOAD] Received ${allPlaces.length} places`);
      
      if (allPlaces.length > 0) {
        console.log("[LOAD] First place sample:", {
          name: allPlaces[0].name,
          category: allPlaces[0].category,
          type: allPlaces[0].type,
          rating: allPlaces[0].rating,
          tags: allPlaces[0].tags
        });
      }
      
      filteredPlaces = [...allPlaces].sort((a, b) => (b.rating || 0) - (a.rating || 0));
      console.log(`[LOAD] Set filteredPlaces to ${filteredPlaces.length} items`);
      
    } catch (err) {
      console.error("Lỗi tải dữ liệu:", err);
      allPlaces = [];
      filteredPlaces = [];
    }
    isLoading = false;
  }

  function filterPlaces() {
    console.log("[FILTER] Starting filter...");
    console.log("[FILTER] allPlaces:", allPlaces.length);
    console.log("[FILTER] selectedCategories:", selectedCategories);
    console.log("[FILTER] minRating:", minRating);

    if (!province || allPlaces.length === 0) {
      filteredPlaces = [];
      console.log("[FILTER] No data to filter");
      return;
    }

    let filtered = allPlaces;

    if (selectedCategories.length > 0 && !selectedCategories.includes("all")) {
      filtered = filtered.filter(place => {
        const placeCategory = place.category || "";
        const placeType = place.type || "";
      
        return selectedCategories.some(cat =>
          placeCategory.toLowerCase().includes(cat.toLowerCase()) ||
          placeType.toLowerCase().includes(cat.toLowerCase())
        );
      });
      console.log(`[FILTER] After category: ${filtered.length}`);
    }

    if (minRating > 0) {
      filtered = filtered.filter(p => (p.rating || 0) >= minRating);
      console.log(`[FILTER] After rating >= ${minRating}: ${filtered.length}`);
    }
  
    filtered = filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    filteredPlaces = filtered;
    console.log(`[FILTER] Final results: ${filteredPlaces.length}`);
  }

  function handleSearch() {
    console.log("[UI] Search button clicked");
    filterPlaces();
  }

  function resetFilters() {
    console.log("[UI] Reset filters");
    selectedCategories = ['all'];
    minRating = 0;
    filteredPlaces = [...allPlaces].sort((a, b) => (b.rating || 0) - (a.rating || 0));
  }

  function handlePlaceClick(place) {
    console.log("[UI] Clicked place:", place.name);
    selectedPlace = place;
    showHotels = false;
    hotels = [];
  }

  function handleBackToList() {
    selectedPlace = null;
    showHotels = false;
    hotels = [];
  }

  async function handleFindHotels() {
    if (!selectedPlace) {
      alert("Vui lòng chọn địa điểm");
      return;
    }
    console.log("[HOTEL] Finding hotels near:", selectedPlace.name);
    console.log("[HOTEL] Place ID:", selectedPlace.id);
    isLoadingHotels = true;
    showHotels = true;
    
    try {
      const hotelData = await getHotelsNearPlace(selectedPlace.id, 50);
      hotels = hotelData;
      console.log(`[HOTEL] Found ${hotels.length} hotels`);
    } catch (error) {
      console.error("[HOTEL] Error fetching hotels:", error);
      alert("Có lỗi xảy ra khi tìm khách sạn: " + error.message);
    } finally {
      isLoadingHotels = false;
    }
  }

  function handleCloseHotels() {
    showHotels = false;
    hotels = [];
  }

  function openGoogleMaps(link) {
    if (link) {
      window.open(link, '_blank');
    }
  }

  $: if (province) {
    console.log("[REACTIVE] Province changed to:", province);
    loadPlacesData();
    selectedPlace = null;
    showHotels = false;
    hotels = [];
  }

  $: console.log("[DEBUG] State:", {
    province,
    allPlaces: allPlaces.length,
    filteredPlaces: filteredPlaces.length,
    isLoading,
    showHotels,
    hotelsCount: hotels.length
  });
</script>

{#if province}
  <div class="info-container">
    {#if isLoading}
      <div class="loading">
        <div class="spinner"></div>
        <p>Đang tải dữ liệu...</p>
      </div>

    {:else if !selectedPlace}
      
      <div class="province-header">
        <h2>{province}</h2>
        <button on:click={resetFilters} class="reset-btn">Reset bộ lọc</button>
      </div>

      <div class="filter-section">
        <h3>Lọc theo danh mục:</h3>
        <div class="categories">
          {#each categories as category}
            <label class="category-checkbox">
              <input type="checkbox" bind:group={selectedCategories} value={category.id} />
              <span>{category.label}</span>
            </label>
          {/each}
        </div>

        <div class="rating-filter">
          <label>Đánh giá tối thiểu: {minRating.toFixed(1)} ⭐</label>
          <input type="range" min="0" max="5" step="0.5" bind:value={minRating} />
        </div>

        <div class="search-actions">
          <button class="search-btn" on:click={handleSearch}>
            Tìm kiếm ({filteredPlaces.length} kết quả)
          </button>
        </div>
      </div>

      <div class="places-list">
        <h3>Địa điểm du lịch ({filteredPlaces.length})</h3>

        {#if filteredPlaces.length > 0}
          <div class="places-grid">
            {#each filteredPlaces as place}
              <div class="place-card" on:click={() => handlePlaceClick(place)}>
                {#if place.image_url}
                  <img src={place.image_url} alt={place.name} />
                {:else}
                  <div class="no-image">📷</div>
                {/if}

                <div class="place-info">
                  <h4>{place.name}</h4>
                  <div class="place-meta">
                    <span class="category-badge">{place.category || 'Không có'}</span>
                    <span class="rating">⭐ {place.rating || 0} ({place.review_count || 0})</span>
                  </div>
                  <p class="place-description">
                    {place.description ? place.description.slice(0, 100) + '...' : 'Không có mô tả'}
                  </p>

                  <div class="place-tags">
                    {#each place.tags ? place.tags.slice(0, 3) : [] as tag}
                      <span class="tag">{tag}</span>
                    {/each}
                  </div>
                </div>
              </div>
            {/each}
          </div>

        {:else if allPlaces.length > 0}
          <p class="no-results">
            Không tìm thấy địa điểm nào phù hợp với bộ lọc.<br>
            <button on:click={resetFilters} style="margin-top: 10px; padding: 8px 16px;">
              Hiển thị tất cả {allPlaces.length} địa điểm
            </button>
          </p>
        {:else}
          <p class="no-results">Không có dữ liệu địa điểm cho tỉnh này.</p>
        {/if}
      </div>

    {:else}
      <div class="place-detail">
        <button class="back-btn" on:click={handleBackToList}>Quay lại</button>

        {#if selectedPlace.image_url}
          <img src={selectedPlace.image_url} class="detail-image" />
        {:else}
          <div class="no-image detail-no-image">📷</div>
        {/if}

        <h2>{selectedPlace.name}</h2>

        <div class="detail-meta">
          <span class="detail-category">{selectedPlace.category || 'Không có'}</span>
          <span class="detail-rating">
            ⭐ {selectedPlace.rating || 0} ({selectedPlace.review_count || 0} đánh giá)
          </span>
        </div>

        <div class="detail-section">
          <h4>Mô tả</h4>
          <p>{selectedPlace.description || 'Không có mô tả'}</p>
        </div>

        <div class="detail-section">
          <h4>Địa chỉ</h4>
          <p>{selectedPlace.address || 'Không có địa chỉ'}</p>
          <button class="hotel-btn" on:click={handleFindHotels}>
            {isLoadingHotels ? 'Đang tìm...' : 'Tìm khách sạn gần đây'}
          </button>
        </div>

        {#if showHotels}
          <div class="hotels-box">
            <div class="hotels-header">
              <h3>Khách sạn gần {selectedPlace.name}</h3>
              <button class="close-btn" on:click={handleCloseHotels}>×</button>
            </div>
            
            {#if isLoadingHotels}
              <div class="loading-hotels">
                <div class="small-spinner"></div>
                <p>Đang tìm khách sạn...</p>
              </div>
            {:else if hotels.length > 0}
              <div class="hotels-list">
                {#each hotels as hotel, index}
                  <div class="hotel-card">
                    <div class="hotel-info">
                      <h4>{index + 1}. {hotel.hotel}</h4>
                      <p class="hotel-address">{hotel.address || 'Không có địa chỉ'}</p>
                      {#if hotel.distance !== undefined}
                        <p class="hotel-distance">Cách {selectedPlace.name} {hotel.distance.toFixed(1)}km</p>
                      {/if}
                      {#if hotel.description}
                        <p class="hotel-description">{hotel.description}</p>
                      {/if}
                    </div>
                  </div>
                {/each}
              </div>
              
              <div class="hotels-summary">
                <p>Tìm thấy <strong>{hotels.length}</strong> khách sạn trong bán kính 50km</p>
              </div>
            {:else}
              <div class="no-hotels">
                <p>Không tìm thấy khách sạn nào trong bán kính 50km</p>
              </div>
            {/if}
          </div>
        {/if}

        <div class="detail-section">
          <h4>Giờ mở cửa</h4>
          <p>{selectedPlace.open_hours || 'Không có thông tin'}</p>
        </div>

        {#if selectedPlace.highlights?.length > 0}
          <div class="detail-section">
            <h4>Điểm nổi bật</h4>
            <div class="highlight-list">
              {#each selectedPlace.highlights as h}
                <span class="highlight">{h}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if selectedPlace.food?.length > 0}
          <div class="detail-section">
            <h4>Ẩm thực địa phương</h4>
            <div class="food-list">
              {#each selectedPlace.food as item}
                <span class="food-item">🍴 {item}</span>
              {/each}
            </div>
          </div>
        {/if}

        {#if selectedPlace.tags?.length > 0}
          <div class="detail-section">
            <h4>Thẻ</h4>
            <div class="tags-list">
              {#each selectedPlace.tags as tag}
                <span class="tag">{tag}</span>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    {/if}
  </div>

{:else}
  <div class="placeholder">
    <h3>Click vào một tỉnh trên bản đồ để xem thông tin</h3>
  </div>
{/if}

<style>
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #4CAF50;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .reset-btn {
    background: #6c757d;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    margin-left: 10px;
  }
  
  .search-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
  }
  
  .no-image {
    width: 100%;
    height: 150px;
    background: #f0f0f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
  }
  
  .detail-no-image {
    height: 250px;
    font-size: 60px;
  }
  
  .info-container {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    max-height: 80vh;
    overflow-y: auto;
  }
  
  .province-header {
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #4CAF50;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .province-header h2 {
    margin: 0;
    color: #2c3e50;
  }
  
  .filter-section {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .categories {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 10px 0;
  }
  
  .category-checkbox {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    padding: 5px 10px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 20px;
    transition: all 0.3s;
  }
  
  .category-checkbox:hover {
    border-color: #4CAF50;
  }
  
  .category-checkbox input {
    margin: 0;
  }
  
  .rating-filter {
    margin: 15px 0;
  }
  
  .rating-filter input {
    width: 100%;
    margin-top: 5px;
  }
  
  .search-btn {
    width: 100%;
    padding: 12px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .search-btn:hover {
    background: #45a049;
  }
  
  .places-list {
    margin-top: 20px;
  }
  
  .places-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
    margin-top: 15px;
  }
  
  .place-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    background: white;
  }
  
  .place-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  .place-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
  }
  
  .place-info {
    padding: 15px;
  }
  
  .place-info h4 {
    margin: 0 0 10px 0;
    color: #2c3e50;
  }
  
  .place-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .category-badge {
    background: #e3f2fd;
    color: #1976d2;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
  }
  
  .rating {
    color: #ff9800;
    font-weight: bold;
  }
  
  .place-description {
    color: #666;
    font-size: 14px;
    margin: 10px 0;
    line-height: 1.4;
  }
  
  .place-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 10px;
  }
  
  .tag {
    background: #f1f8e9;
    color: #689f38;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
  }
  
  .no-results {
    text-align: center;
    padding: 30px;
    color: #666;
    font-style: italic;
  }
  
  .placeholder {
    text-align: center;
    padding: 40px 20px;
    color: #666;
  }
  
  .placeholder h3 {
    color: #4CAF50;
  }
  
  .place-detail {
    animation: fadeIn 0.3s ease-in;
  }
  
  .back-btn {
    background: #6c757d;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 20px;
    font-size: 14px;
  }
  
  .back-btn:hover {
    background: #5a6268;
  }
  
  .detail-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .detail-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 15px 0;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .detail-category {
    background: #4CAF50;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
  }
  
  .detail-rating {
    font-size: 18px;
    color: #ff9800;
    font-weight: bold;
  }
  
  .detail-section {
    margin: 20px 0;
    padding: 15px;
    border-left: 4px solid #4CAF50;
    background: #f8f9fa;
    border-radius: 0 8px 8px 0;
  }
  
  .detail-section h4 {
    margin: 0 0 10px 0;
    color: #2c3e50;
  }
  
  .highlight-list, .food-list, .tags-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
  }
  
  .highlight {
    background: #e8f5e9;
    color: #2e7d32;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .food-item {
    background: #fff3e0;
    color: #ef6c00;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 14px;
  }
  
  .hotel-btn {
    display: block;
    width: 100%;
    margin-top: 15px;
    padding: 12px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }
  
  .hotel-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  }
  
  .hotel-btn:active {
    transform: translateY(0);
  }
  
  .hotels-box {
    margin: 20px 0;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
    border: 2px solid #4CAF50;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    animation: slideIn 0.3s ease-out;
  }
  
  .hotels-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
  }
  
  .hotels-header h3 {
    margin: 0;
    color: #2c3e50;
    font-size: 18px;
  }
  
  .close-btn {
    color: black;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .loading-hotels {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  
  .small-spinner {
    width: 30px;
    height: 30px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #4CAF50;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }
  
  .hotels-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .hotel-card {
    background: white;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s;
  }
  
  .hotel-card:hover {
    transform: translateX(5px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
  
  .hotel-info {
    flex: 1;
  }
  
  .hotel-info h4 {
    margin: 0 0 8px 0;
    color: #2c3e50;
    font-size: 16px;
  }
  
  .hotel-address, .hotel-distance, .hotel-description {
    margin: 4px 0;
    font-size: 14px;
    color: #666;
  }
  
  .hotel-distance {
    color: #ff9800;
    font-weight: bold;
  }
  
  .map-btn {
    background: #28a745;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    margin-left: 15px;
    white-space: nowrap;
  }
  
  .map-btn:hover {
    background: #218838;
  }
  
  .hotels-summary {
    margin-top: 15px;
    padding: 10px;
    background: #e8f5e9;
    border-radius: 6px;
    text-align: center;
    color: #2e7d32;
    font-size: 14px;
  }
  
  .no-hotels {
    text-align: center;
    padding: 20px;
    color: #666;
  }
  
  .no-hotels p {
    margin: 10px 0;
  }
  
  .suggestion {
    font-style: italic;
    color: #6c757d;
  }
  
  .search-suggestion {
    background: #fff3cd;
    padding: 10px;
    border-radius: 6px;
    border-left: 4px solid #ffc107;
    font-weight: bold;
    color: #856404;
  }
  
  .external-search-btn {
    margin-top: 15px;
    padding: 10px 20px;
    background: #ff9800;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .external-search-btn:hover {
    background: #e68900;
  }
  
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
</style>