// food.js
export async function getFoodsByProvinceAndTag(province, tag) {
  try {
    console.log(`[FOOD API] Fetching foods for: province="${province}", tag="${tag}"`);
    
    const url = `http://localhost:8000/foods/foods/?province=${encodeURIComponent(province)}&tag=${encodeURIComponent(tag)}`;
    console.log(`[FOOD API] URL: ${url}`);
    
    const response = await fetch(url);
    console.log(`[FOOD API] Response status: ${response.status}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`[FOOD API] Received ${data.length} foods`);
    return data;
    
  } catch (error) {
    console.error("Error fetching foods:", error);
    throw error;
  }
}

// THÊM HÀM MỚI ĐỂ LẤY DANH SÁCH TAG CHÍNH
export async function getMainFoodTags(province) {
  try {
    console.log(`[FOOD API] Fetching main food tags for: province="${province}"`);
    
    const url = `http://localhost:8000/foods/foods/tags/main?province=${encodeURIComponent(province)}`;
    console.log(`[FOOD API] URL: ${url}`);
    
    const response = await fetch(url);
    console.log(`[FOOD API] Response status: ${response.status}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`[FOOD API] Received ${data.length} main tags`);
    return data;
    
  } catch (error) {
    console.error("Error fetching main food tags:", error);
    throw error;
  }
}