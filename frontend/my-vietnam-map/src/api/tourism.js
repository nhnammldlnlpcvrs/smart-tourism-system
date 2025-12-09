const API = "http://127.0.0.1:8000";

export async function getPlacesByProvince(province) {
    const res = await fetch(`${API}/tourism/by-province/${province}`);
    return res.json();
}

export async function getPlaceDetail(id) {
    const res = await fetch(`${API}/tourism/${id}`);
    return res.json();
}

export async function getCategoryTree(province) {
    const res = await fetch(`${API}/tourism/tags?province=${province}`);
    return res.json();
}
