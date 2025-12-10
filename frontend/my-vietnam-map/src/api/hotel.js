// frontend/src/api/hotel.js
const BASE_URL = 'http://localhost:8000';

export async function getHotelsNearPlace(placeId, radius = 50) {
  try {
    const url = `${BASE_URL}/hotels/hotels/?place_id=${placeId}&radius=${radius}`;
    console.log('[HOTEL API] Fetching:', url);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('[HOTEL API] Response:', data);
    return data;
  } catch (error) {
    console.error('[HOTEL API] Error:', error);
    return [];
  }
}