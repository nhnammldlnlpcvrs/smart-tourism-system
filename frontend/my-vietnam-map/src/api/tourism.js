const API = "http://127.0.0.1:8000";

// Lấy danh sách tỉnh/thành
export async function getProvinces() {
    try {
        const res = await fetch(`${API}/tourism/tourism/provinces`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        return data.provinces || data || [];
    } catch (error) {
        console.error("Error fetching provinces:", error);
        return [];
    }
}

// Lấy danh sách categories theo tỉnh
export async function getCategoryTree(province) {
    try {
        const res = await fetch(
            `${API}/tourism/tourism/categories?province=${encodeURIComponent(province)}`
        );
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        return data.categories || data || [];
    } catch (error) {
        console.error(`Error fetching categories for ${province}:`, error);
        return [];
    }
}

// Lấy all địa điểm của một tỉnh 
export async function getPlacesByProvince(province) {
    try {
        // GỌI API với chỉ province, không có subcategories
        const url = `${API}/tourism/tourism/places?province=${encodeURIComponent(province)}`;
        console.log("[API] START Fetching all places for province:", province);
        console.log("[API] URL:", url);
        
        const res = await fetch(url);
        
        console.log("[API] Response status:", res.status, res.statusText);
        
        if (!res.ok) {
            console.error(`[API] HTTP ${res.status} for: ${url}`);
            const errorText = await res.text();
            console.error(`[API] Error response:`, errorText);
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        console.log("[API] Full response data:", data);
        console.log("[API] Results count:", data.results ? data.results.length : 0);
        
        if (data.results && Array.isArray(data.results)) {
            console.log("[API] First result sample:", {
                name: data.results[0]?.name,
                category: data.results[0]?.category,
                rating: data.results[0]?.rating
            });
            return data.results;
        } else {
            console.warn("[API] Unexpected response structure, returning empty array");
            return [];
        }
        
    } catch (error) {
        console.error(`[API] Error fetching places for ${province}:`, error);
        return [];
    }
}

// Lấy địa điểm theo tỉnh VÀ subcategory cụ thể
export async function getPlacesByProvinceAndCategory(province, subcategories = null) {
    try {
        let url = `${API}/tourism/tourism/places?province=${encodeURIComponent(province)}`;
        
        if (subcategories && Array.isArray(subcategories) && subcategories.length > 0) {
            subcategories.forEach(cat => {
                url += `&subcategories=${encodeURIComponent(cat)}`;
            });
        }
        
        console.log("[API] Fetching filtered places:", url);
        const res = await fetch(url);
        
        if (!res.ok) {
            console.error(`[API] HTTP ${res.status} for: ${url}`);
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        return data.results || [];
    } catch (error) {
        console.error(`[API] Error fetching filtered places for ${province}:`, error);
        return [];
    }
}